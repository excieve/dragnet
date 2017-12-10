import logging
import argparse
import pandas
import numpy

from cloudant import couchdb
from elasticsearch import Elasticsearch
from elasticsearch.helpers import parallel_bulk


logger = logging.getLogger('dragnet.pump')


def load_processed(filename, match_field):
    """
    Loads processing results, filters by state if needed and returns a Pandas DataFrame.
    """
    df = pandas.read_csv(filename, na_filter=False, index_col=match_field)
    return df


def load_state(filename):
    """
    Loads last imported state and returns it as a set for efficient existence queries.
    """
    ids = []
    with open(filename, 'r', encoding='utf-8') as state_file:
        ids = state_file.read().splitlines()
    return set(ids)


def map_row_to_esop(doc, state, processed, match_field, container_field, es_config):
    """
    Maps CouchDB document to ElasticSearch Bulk API operation, while matching with a processed result if available.
    Returns a dict with formatted "upsert".
    """
    def np_to_scalar(v):
        if isinstance(v, numpy.generic):
            return numpy.asscalar(v)
        else:
            return v

    doc['couchdb_id'] = doc.pop('_id')  # ES doesn't allow "_id" as it is its own metadata
    try:
        processed_doc = processed.loc[doc['doc_uuid']]
        # Getting rid of numpy types before passing over to ES JSON serialiser
        doc[container_field] = dict(
            (k, np_to_scalar(v)) for k, v in processed_doc.items()
        )
    except KeyError:
        pass
    op = {
        '_op_type': 'update',  # Upserts for the win
        '_index': es_config['index'],
        '_type': es_config['doc_type'],
        '_id': doc.pop('doc_uuid'),
        'doc': doc,
        'doc_as_upsert': True
    }

    return op


def csv_to_elasticsearch(processed_filename, state_filename, match_field, container_field, db_config, es_config):
    logger.info('Pumping state "{}" and processing results CSV "{}" to "{}" container field in related documents'
                .format(state_filename, processed_filename, container_field))
    es = Elasticsearch(es_config['endpoint'], timeout=120, maxsize=16)
    with couchdb(db_config['user'], db_config['password'], url=db_config['url']) as couch:
        db = couch[db_config['name']]
        state = load_state(state_filename)
        logger.info('Loaded {} IDs from the last imported state.'.format(len(state)))
        if not state:
            return
        processed = load_processed(processed_filename, match_field)
        logger.info('Loaded {} processed results.'. format(len(processed)))
        state_list = sorted(list(state))  # Sorting is important to utilise B-Tree slicing in CouchDB
        first_result = db[state_list[0]]
        start_key = state_list[0]
        end_key = state_list[-1]
        logger.info('Docs with keys between "{}" and "{}" will be pumped to ES.'.format(start_key, end_key))
        del state_list
        rows_pumped = 0

        if len(state) > 20000:
            bulk_accumulator = [
                map_row_to_esop(first_result, state, processed, match_field, container_field, es_config)
            ]

            with db.custom_result(skip=1, limit=4800, include_docs=True) as result:
                reached_end = False
                while not reached_end:
                    rows = result[start_key:]
                    if rows:
                        start_key = rows[-1]['key']
                        for row in rows:
                            if row['id'] in state:
                                doc = map_row_to_esop(
                                    row['doc'], state, processed, match_field, container_field, es_config)
                                bulk_accumulator.append(doc)
                            if row['id'] == end_key:
                                # Reached the end of state, no point looking further
                                reached_end = True
                                break
                        # Consume the parallel generator in full
                        # TODO: make threads and chunks configurable
                        for success, info in parallel_bulk(es, bulk_accumulator, thread_count=16, chunk_size=300):
                            if success:
                                rows_pumped += 1
                            else:
                                logger.warning('Pumping documents failed: {}'.format(info))
                        logger.info('Pump processed {} rows.'.format(rows_pumped))

                        bulk_accumulator = []
        else:
            with db.custom_result(keys=list(state), include_docs=True) as result:
                bulk_accumulator = [
                    map_row_to_esop(row['doc'], state, processed, match_field, container_field, es_config)
                    for row in result
                ]
                # TODO: make threads and chunks configurable
                for success, info in parallel_bulk(es, bulk_accumulator, thread_count=16, chunk_size=300):
                    if success:
                        rows_pumped += 1
                    else:
                        logger.warning('Pumping documents failed: {}'.format(info))
                logger.info('Pump processed {} rows.'.format(rows_pumped))

        logger.info('Total pumped/state/processing: {}/{}/{}.'.format(rows_pumped, len(state), len(processed)))


if __name__ == '__main__':
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)

    parser = argparse.ArgumentParser(description='Pump CSV to ElasticSearch index')
    parser.add_argument('filename', help='CSV filename')
    parser.add_argument('-u', '--username', help='CouchDB username')
    parser.add_argument('-p', '--password', help='CouchDB password')
    parser.add_argument('-d', '--dbname', help='CouchDB database name', default='declarations')
    parser.add_argument('-e', '--endpoint', help='CouchDB endpoint', default='http://localhost:5984')
    parser.add_argument('-E', '--elasticsearch', help='ElasticSearch endpoint', default='http://localhost:9200')
    parser.add_argument('-i', '--index', help='ElasticSearch index')
    parser.add_argument('-t', '--type', help='ElasticSearch doctype')
    parser.add_argument('-m', '--match', help='CSV match field')
    parser.add_argument('-c', '--container', help='Container field in ES doctype')
    parser.add_argument('-S', '--state', help='Filename with imported IDs')
    args = parser.parse_args()

    db_config = {
        'user': args.username,
        'password': args.password,
        'url': args.endpoint,
        'name': args.dbname
    }

    es_config = {
        'endpoint': args.elasticsearch,
        'index': args.index,
        'doc_type': args.type
    }

    csv_to_elasticsearch(args.filename, args.state, args.match, args.container, db_config, es_config)
