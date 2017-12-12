import logging
import argparse
import csv

from cloudant import couchdb

from misc import load_state

logger = logging.getLogger('dragnet.export')


def write_row(row, writer):
    keys = []
    if isinstance(row['key'], list):
        keys = row['key']
    values = row['value']
    if not isinstance(values, list):
        values = [values]
    writer.writerow(keys + values)


def export_view(filename, state_filename, design_doc_name, view_name, db_config, mappings=None):
    with couchdb(db_config['user'], db_config['password'], url=db_config['url']) as couch:
        db = couch[db_config['name']]
        design_doc = db.get_design_document(design_doc_name)
        view = design_doc.get_view(view_name)

        logger.info('Found view "{}" in design doc "{}".'.format(view.view_name, design_doc_name))
        first_result = view(stale='ok', limit=1)
        logger.info('This view contains {} rows, exporting...'.format(first_result['total_rows']))

        rows_exported = 0
        if state_filename is not None:
            state = load_state(state_filename)
        else:
            state = None

        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            view_writer = csv.writer(csvfile)
            if mappings:
                view_writer.writerow(mappings)
            # Instead of using offsets and limits to get batches we're utilising B-Tree properly:
            # http://docs.couchdb.org/en/2.0.0/couchapp/views/pagination.html#paging-alternate-method
            # This scales very well as the DB never needs to scan over all the previous nodes.

            if state is None or len(state) > 20000:
                rows = first_result['rows']
                if rows:
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
            else:
                with view.custom_result(keys=state, stale='ok') as result:
                    for row in result:
                        write_row(row, view_writer)
                        rows_exported += 1
                    logger.info('Exported {} rows.'.format(rows_exported))
        logger.info('Total exported {} rows. '.format(rows_exported))


if __name__ == '__main__':
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)

    parser = argparse.ArgumentParser(description='Export document from CouchDB view to a CSV file')
    parser.add_argument('designdoc', help='Design document')
    parser.add_argument('view', help='View name')
    parser.add_argument('-u', '--username', help='CouchDB username')
    parser.add_argument('-p', '--password', help='CouchDB password')
    parser.add_argument('-d', '--dbname', help='CouchDB database name', default='declarations')
    parser.add_argument('-e', '--endpoint', help='CouchDB endpoint', default='http://localhost:5984')
    parser.add_argument('-o', '--output', help='Output file name', required=True)
    parser.add_argument('-S', '--state', help='Only export documents with IDs from a provided file')
    args = parser.parse_args()

    db_config = {
        'user': args.username,
        'password': args.password,
        'url': args.endpoint,
        'name': args.dbname,
        'design_doc': args.designdoc,
        'view': args.view
    }

    export_view(args.output, args.state, args.designdoc, args.view, db_config)
