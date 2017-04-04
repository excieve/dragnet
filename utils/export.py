import logging
import argparse
import csv

from cloudant import couchdb

logging.basicConfig()
logger = logging.getLogger('dragnet.export')
logger.setLevel(logging.INFO)


# TODO: possibly take this as an argument in some form
HEADER_MAP = {
    'step_3_estate': ['id', 'person', 'type', 'same_year', 'foreign', 'ownership', 'quant', 'space', 'max_space',
                      'cost_purch', 'cost_last'],
    'step_6_vehicles': ['id', 'person', 'type', 'same_year', 'ownership', 'quant', 'cost', 'max_cost', 'max_year',
                        'brand_models'],
    'step_11_income': ['id', 'person', 'type', 'foreign', 'value'],
    'step_12_assets': ['id', 'person', 'type', 'foreign', 'currency', 'value'],
    'meta': ['id', 'link', 'name', 'work_post', 'work_place', 'year', 'name_post', 'family', 'organization_group',
             'region']
}


def export_view(filename, db_config):
    with couchdb(db_config['user'], db_config['password'], url=db_config['url']) as couch:
        db = couch[db_config['name']]
        design_doc = db.get_design_document(db_config['design_doc'])
        view = design_doc.get_view(db_config['view'])

        logger.info('Found view "{}" in design doc "{}".'.format(view.view_name, db_config['design_doc']))
        zero_result = view(stale='ok', limit=0)
        logger.info('This view contains {} rows, exporting...'.format(zero_result['total_rows']))

        rows_exported = 0
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            view_writer = csv.writer(csvfile)
            view_writer.writerow(HEADER_MAP[db_config['design_doc']])
            # TODO: pagination with "skip" as this client does is rather slow on large "skip" values with small limit,
            # this is the reason we're using huge "page_size". This is still suboptimal though and will only work with
            # small view rows. There's an alternative to try later, which should work better, utilising B-Tree properly:
            # http://docs.couchdb.org/en/2.0.0/couchapp/views/pagination.html#paging-alternate-method
            with view.custom_result(page_size=100000, stale='ok') as result:
                for row in result:
                    keys = row['key']
                    if not isinstance(keys, list):
                        keys = [keys]
                    values = row['value']
                    if not isinstance(values, list):
                        values = [values]
                    view_writer.writerow(keys + values)
                    rows_exported += 1
                    if rows_exported % 10000 == 0:
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
