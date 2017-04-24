import logging
import argparse
import csv

from cloudant import couchdb

logging.basicConfig()
logger = logging.getLogger('dragnet.export')
logger.setLevel(logging.INFO)


# TODO: possibly take this as an argument in some form
HEADER_MAP = {
    'step_3_estate': ['id', 'estate.person', 'estate.type', 'estate.same_year', 'estate.foreign', 'estate.ownership',
                      'estate.quant', 'estate.space', 'estate.max_space', 'estate.cost_purch', 'estate.cost_last'],
    'step_3_estate_agg': ['id', 'estate.declarant_land', 'estate.declarant_other', 'estate.family_land',
                          'estate.family_other', 'estate.total_land', 'estate.total_other', 'estate.has_hidden',
                          'estate.has_foreign'],
    'step_6_vehicles': ['id', 'vehicles.person', 'vehicles.type', 'vehicles.same_year', 'vehicles.ownership',
                        'vehicles.quant', 'vehicles.cost', 'vehicles.max_cost', 'vehicles.max_year',
                        'vehicles.brand_models'],
    'step_6_vehicles_agg': ['id', 'vehicles.declarant_cost', 'vehicles.family_cost', 'vehicles.total_cost',
                            'vehicles.max_year', 'vehicles.has_hidden', 'vehicles.all_names', 'vehicles.any'],
    'step_11_incomes': ['id', 'income.person', 'income.type', 'income.foreign', 'income.value'],
    'step_11_incomes_agg': ['id', 'incomes.declarant', 'incomes.family', 'incomes.total', 'incomes.has_hidden',
                            'incomes.has_foreign'],
    'step_12_assets': ['id', 'assets.person', 'assets.type', 'assets.foreign', 'assets.currency', 'assets.value'],
    'step_12_assets_agg': ['id', 'assets.declarant', 'assets.family', 'assets.total', 'assets.has_hidden',
                           'assets.has_foreign'],
    'meta': ['id', 'link', 'name', 'year', 'name_post', 'family', 'organization_group',
             'region']
}


def write_row(row, writer):
    keys = row['key']
    if not isinstance(keys, list):
        keys = [keys]
    values = row['value']
    if not isinstance(values, list):
        values = [values]
    writer.writerow(keys + values)


def export_view(filename, db_config):
    with couchdb(db_config['user'], db_config['password'], url=db_config['url']) as couch:
        db = couch[db_config['name']]
        design_doc = db.get_design_document(db_config['design_doc'])
        view = design_doc.get_view(db_config['view'])

        logger.info('Found view "{}" in design doc "{}".'.format(view.view_name, db_config['design_doc']))
        first_result = view(stale='ok', limit=1)
        logger.info('This view contains {} rows, exporting...'.format(first_result['total_rows']))

        rows_exported = 0
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            view_writer = csv.writer(csvfile)
            view_writer.writerow(HEADER_MAP[db_config['design_doc']])
            # Instead of using offsets and limits to get batches we're utilising B-Tree properly:
            # http://docs.couchdb.org/en/2.0.0/couchapp/views/pagination.html#paging-alternate-method
            # This scales very well as the DB never needs to scan over all the previous nodes.
            rows = first_result['rows']
            start_key = rows[0]['key']
            write_row(rows[0], view_writer)
            rows_exported += 1
            with view.custom_result(skip=1, limit=20000, stale='ok') as result:
                while rows:
                    rows = result[start_key:]
                    if rows:
                        start_key = rows[-1]['key']
                        for row in rows:
                            write_row(row, view_writer)
                            rows_exported += 1
                        logger.info('Exported {} rows.'.format(rows_exported))
        logger.info('Total exported {} rows. '.format(rows_exported))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Export document from CouchDB view to a CSV file')
    parser.add_argument('designdoc', help='Design document')
    parser.add_argument('view', help='View name')
    parser.add_argument('-u', '--username', help='CouchDB username')
    parser.add_argument('-p', '--password', help='CouchDB password')
    parser.add_argument('-d', '--dbname', help='CouchDB database name', default='declarations')
    parser.add_argument('-e', '--endpoint', help='CouchDB endpoint', default='http://localhost:5984')
    parser.add_argument('-o', '--output', help='Output file name', required=True)
    args = parser.parse_args()

    db_config = {
        'user': args.username,
        'password': args.password,
        'url': args.endpoint,
        'name': args.dbname,
        'design_doc': args.designdoc,
        'view': args.view
    }

    export_view(args.output, db_config)
