import logging
import argparse
import json
import importlib.util
import os.path
import sys

from load import import_all
from addview import load_source, add_function
from export import export_view
from merge import merge_csv
from pump import csv_to_elasticsearch

logger = logging.getLogger('dragnet.profile')


def loader(profile, db_config, concurrency, chunks_per_process):
    loader_profile = profile['loader']
    assert loader_profile['type'] == 'nacp', 'Unsupported loader type'

    logger.info('Executing loader...')
    import_all(loader_profile['input_dir'], db_config, concurrency, chunks_per_process, loader_profile['state_file'])


def runner(profile, db_config):
    runner_profile = profile['runner']
    assert runner_profile['type'] in ['chakra', 'javascript'], 'Unsupported runner type'

    logger.info('Executing view runners...')
    exec_stats = []
    for design_doc in runner_profile['design_documents']:
        logger.info('Processing design document "{}":'.format(design_doc['name']))
        for view in design_doc['views']:
            view_name = os.path.splitext(os.path.basename(view))[0]
            logger.info('Loading and executing view "{}"...'.format(view_name))
            map_function_source, _ = load_source(view)
            func_db_config = {
                'design_doc': design_doc['name'],
                'view': view_name
            }
            func_db_config.update(db_config)
            exec_stat = add_function(map_function_source, reduce_function_source=None, db_config=func_db_config,
                                     language=runner_profile['type'], execute=runner_profile['sequential'])
            exec_stats.append(exec_stat)
    return exec_stats


def exporter(profile, db_config):
    exporter_profile = profile['exporter']
    assert exporter_profile['type'] == 'csv', 'Unsupported exporter type'

    logger.info('Executing exporters...')
    for mapping in exporter_profile['mappings']:
        design_doc, view = mapping['view'].split('.')
        export_view(mapping['output'], design_doc, view, db_config, mapping.get('columns'))


def merger(profile):
    merger_profile = profile['merger']
    assert merger_profile['type'] == 'csv', 'Unsupported merger type'

    logger.info('Executing merger...')
    # Load and exec a Python module containing the Pandas filters
    filter_func = None
    if merger_profile.get('outlier_filters'):
        logger.info('Loading Pandas filters for outlier detection.')
        spec = importlib.util.spec_from_file_location('outlier_filters', merger_profile['outlier_filters'])
        outlier_filters = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(outlier_filters)
        filter_func = outlier_filters.filter_func

    merge_csv(merger_profile['output'], merger_profile['inputs'], merger_profile['field'],
              merger_profile.get('nan_replacements'), filter_func, merger_profile.get('only_years'))


def pump(profile, db_config, es_endpoint):
    pump_profile = profile['pump']
    assert pump_profile['type'] == 'csv_to_elasticsearch', 'Unsupported pump type'

    logger.info('Executing pump...')
    es_config = {
        'endpoint': es_endpoint,
        'index': pump_profile['index'],
        'doc_type': pump_profile['doc_type']
    }
    csv_to_elasticsearch(pump_profile['input'], pump_profile['state_file'], pump_profile['match_field'],
                         pump_profile['container_field'], db_config, es_config)


if __name__ == '__main__':
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)

    parser = argparse.ArgumentParser(description='Execute a Dragnet profile')
    parser.add_argument('action',
                        help='Action to execute (use "all" to sequentially perform every action except "loader")',
                        choices=['all', 'loader', 'runner', 'exporter', 'merger', 'pump'])
    parser.add_argument('profile', help='Profile to execute')
    parser.add_argument('-d', '--datadir', help='Data directory', default='data')
    parser.add_argument('-u', '--username', help='CouchDB username')
    parser.add_argument('-p', '--password', help='CouchDB password')
    parser.add_argument('-e', '--endpoint', help='CouchDB endpoint', default='http://localhost:5984')
    parser.add_argument('-E', '--elasticsearch', help='ElasticSearch endpoint', default='http://localhost:9200')
    parser.add_argument('-n', '--noreexport', help='Take no further action if no execution was detected',
                        action='store_true', default=False)
    parser.add_argument('-c', '--concurrency', help='Number of processes to spawn', type=int, default=8)
    parser.add_argument('-C', '--chunks', help='Number of chunks to run in a batch', type=int, default=200)
    args = parser.parse_args()

    with open('{}/profiles/{}.json'.format(args.datadir, args.profile), 'r', encoding='utf-8') as fp:
        raw_json = fp.read()
        profile = json.loads(raw_json.replace('{datadir}', args.datadir))

    db_config = {
        'user': args.username,
        'password': args.password,
        'url': args.endpoint,
        'name': profile['database']
    }

    logger.info('Profile "{}" successfully loaded.'.format(profile['name']))

    if args.action == 'loader' and 'loader' in profile:
        loader(profile, db_config, args.concurrency, args.chunks)
    if args.action in ('all', 'runner') and 'runner' in profile:
        exec_stats = runner(profile, db_config)
    if args.noreexport and not any(exec_stats):
        logger.info('No runner execution detected and "noreexport" is set -- preventing further actions.')
        sys.exit(0)
    if args.action in ('all', 'exporter') and 'exporter' in profile:
        exporter(profile, db_config)
    if args.action in ('all', 'merger') and 'merger' in profile:
        merger(profile)
    if args.action in ('all', 'pump') and 'pump' in profile:
        pump(profile, db_config, args.elasticsearch)

    logger.info('Profiles execution complete.')
