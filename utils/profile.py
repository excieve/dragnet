import logging
import argparse
import json
import importlib.util
import os.path
import sys
import pandas

from load import import_all
from addview import load_source, add_function
from export import export_view
from merge import merge_csv
from pump import csv_to_elasticsearch

logger = logging.getLogger('dragnet.profile')


def loader(profile, db_config, concurrency, chunks_per_process):
    loader_profile = profile['loader']
    assert loader_profile['type'] in ('nacp', 'nacp_new_format'), 'Unsupported loader type'

    logger.info('Executing loader...')
    import_all(
        docs_dir=loader_profile['input_dir'],
        corrected_file=loader_profile.get("corrected_file"),
        db_config=db_config, 
        concurrency=concurrency, 
        chunks_per_process=chunks_per_process,
        state_filename=loader_profile['state_file'],
        parser_type=loader_profile['type']
    )


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
        export_view(
            mapping['output'],
            exporter_profile.get("state_file"),
            design_doc,
            view,
            db_config,
            mapping.get('columns')
        )


def merger(profile):
    TYPES_MAPPING = {"Int64Dtype": pandas.Int64Dtype, "bool": "boolean", "float64": "float64"}

    merger_profile = profile["merger"]
    assert merger_profile["type"] == "csv", "Unsupported merger type"

    logger.info("Executing merger...")
    # Load and exec Python modules containing the Pandas functions
    postprocess_funcs = []
    if merger_profile.get("postprocess"):
        logger.info("Loading Pandas post-processing functions.")
        for i, pp_filename in enumerate(merger_profile["postprocess"]):
            logger.info("Loading: {}".format(pp_filename))
            spec = importlib.util.spec_from_file_location(
                "postprocess_module_{}".format(i), pp_filename
            )
            postprocess_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(postprocess_module)
            postprocess_funcs.append(postprocess_module.postprocess_func)

    type_overrides = {}
    if merger_profile.get("type_overrides"):
        for field, dtype in merger_profile["type_overrides"].items():
            assert dtype in TYPES_MAPPING, "Allowed types are {}".format(", ".join(TYPES_MAPPING.keys()))
            if callable(TYPES_MAPPING[dtype]):
                type_overrides[field] = TYPES_MAPPING[dtype]()
            else:
                type_overrides[field] = TYPES_MAPPING[dtype]

    merge_csv(
        merger_profile["output"],
        merger_profile["inputs"],
        merger_profile["field"],
        merger_profile.get("nan_replacements"),
        postprocess_funcs,
        merger_profile.get("only_years"),
        type_overrides
    )


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
                         pump_profile['container_field'], db_config, es_config, pump_profile.get("filter_values"))


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
