import logging
import argparse
import csv

from elasticsearch import Elasticsearch, NotFoundError


logger = logging.getLogger('dragnet.pump')


def csv_to_elasticsearch(filename, match_field, container_field, es_config):
    logger.info('Pumping CSV "{}" to "{}" container field in related ElasticSearch documents'
                .format(filename, container_field))
    es = Elasticsearch(es_config['endpoint'])
    with open(filename, 'r', encoding='utf-8') as input_file:
        reader = csv.DictReader(input_file)
        for row in reader:
            doc_id = row.pop(match_field)
            try:
                # Utilise partial document update to populate the container field. This saves us a lot of bandwidth
                # avoiding full doc transfer back and forth.
                # In case nothing changed ES knows to avoid any operations internally.
                es.update(index=es_config['index'], doc_type=es_config['doc_type'], id=doc_id,
                          body={container_field: row})
            except NotFoundError:
                # This means we're trying to update a document that hasn't propagated to ES yet, just log it for now
                logger.error('Document "{}" does not exist in ES yet, maybe rerun later.'.format(doc_id))


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
        'endpoint': args.endpoint,
        'index': args.index,
        'doc_type': args.type
    }

    csv_to_elasticsearch(args.filename, args.match, args.container, es_config)
