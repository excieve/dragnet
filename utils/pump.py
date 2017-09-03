import logging
import argparse
import csv

from elasticsearch import Elasticsearch, NotFoundError, helpers


logger = logging.getLogger('dragnet.pump')


def csv_to_elasticsearch(filename, match_field, container_field, es_config):
    logger.info('Pumping CSV "{}" to "{}" container field in related ElasticSearch documents'
                .format(filename, container_field))
    es = Elasticsearch(es_config['endpoint'])
    with open(filename, 'r', encoding='utf-8') as input_file:
        reader = csv.DictReader(input_file)
        rows_total = 0
        rows_pumped = 0

        def pump_it(chunk):
            _, errors = helpers.bulk(
                es, chunk,
                raise_on_exception=False, raise_on_error=False,
                chunk_size=1000
            )
            for error in errors:
                # This means we're trying to update a document that hasn't propagated to ES yet, just log it for now
                logger.error(
                    'Document "{}" does not exist in ES yet, maybe rerun later.'.format(error['update']['_id']))

        current_chunk = []
        for row in reader:
            doc_id = row.pop(match_field)
            # Utilise partial document update to populate the container field. This saves us a lot of bandwidth
            # avoiding full doc transfer back and forth.
            # In case nothing changed ES knows to avoid any operations internally.
            # es.update(index=es_config['index'], doc_type=es_config['doc_type'], id=doc_id,
            #           body={'doc': {container_field: row}})
            current_chunk.append({
                '_op_type': 'update',
                '_index': es_config['index'],
                '_type': es_config['doc_type'],
                '_id': doc_id,
                'doc': {container_field: row}
            })

            rows_pumped += 1

            rows_total += 1
            if rows_total % 10000 == 0:
                pump_it(current_chunk)
                current_chunk = []
                logger.info('Pump processed {} rows.'.format(rows_total))

        pump_it(current_chunk)
        logger.info('Total pumped {}/{} rows.'.format(rows_pumped, rows_total))


if __name__ == '__main__':
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)

    parser = argparse.ArgumentParser(description='Pump CSV to ElasticSearch index')
    parser.add_argument('filename', help='CSV filename')
    parser.add_argument('-e', '--elasticsearch', help='ElasticSearch endpoint', default='http://localhost:9200')
    parser.add_argument('-i', '--index', help='ElasticSearch index')
    parser.add_argument('-t', '--type', help='ElasticSearch doctype')
    parser.add_argument('-m', '--match', help='CSV match field')
    parser.add_argument('-c', '--container', help='Container field in ES doctype')
    args = parser.parse_args()

    es_config = {
        'endpoint': args.elasticsearch,
        'index': args.index,
        'doc_type': args.type
    }

    csv_to_elasticsearch(args.filename, args.match, args.container, es_config)
