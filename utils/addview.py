import sys
import argparse
import logging
import subprocess

from cloudant import couchdb

logging.basicConfig()
logger = logging.getLogger('dragnet.addview')
logger.setLevel(logging.INFO)


def coffeescript(func):
    with subprocess.Popen(['coffee', '-b', '-s', '-p'],
                          stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
        output, errors = proc.communicate(func.encode('utf-8'))
    if errors:
        logger.error(errors.encode('utf-8'))
        return None

    output = output.decode('utf-8')
    logger.debug(output)
    return output


def load_source(mapfile_name, reducefile_name):
    map_function_source = None
    with open(mapfile_name, 'r', encoding='utf-8') as f:
        map_function_source = f.read()
    logger.info('Loaded map function, size: {}'.format(len(map_function_source)))

    reduce_function_source = None
    if reducefile_name:
        with open(reducefile_name, 'r', encoding='utf-8') as f:
            reduce_function_source = f.read()
        logger.info('Loaded reduce function, size: {}'.format(len(map_function_source)))

    return map_function_source, reduce_function_source


def process_source(map_function_source, reduce_function_source, language):
    if language == 'coffeescript':
        logger.info('Compiling map function from CoffeeScript...')
        map_function_source = coffeescript(map_function_source)
        logger.info('Done.')
        if reduce_function_source:
            logger.info('Compiling reduce function from CoffeeScript...')
            reduce_function_source = coffeescript(reduce_function_source)
            logger.info('Done.')
    return map_function_source, reduce_function_source


def add_function(map_function_source, reduce_function_source, db_config):
    with couchdb(db_config['user'], db_config['password'], url=db_config['url']) as couch:
        db = couch[db_config['name']]
        design_doc = db.get_design_document(db_config['design_doc'])
        logger.info('Working with design document {} from DB {}.'.format(design_doc['_id'], db.database_name))
        design_doc['language'] = 'javascript'  # For now ensuring we're always dealing with JS in the end
        view = design_doc.get_view(db_config['view'])
        if view is None:
            logger.info('View {} does not exist, creating a new one.'.format(db_config['view']))
            design_doc.add_view(db_config['view'], map_function_source, reduce_function_source)
        else:
            logger.info('View {} exists, updating.'.format(view.view_name))
            design_doc.update_view(db_config['view'], map_function_source, reduce_function_source)
        design_doc.save()
        logger.info('Design doc successfully saved.')
        logger.debug(design_doc.info())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Adds a MapReduce view to CouchDB database design doc')
    parser.add_argument('mapfile', help='File containing the map function source')
    parser.add_argument('-r', '--reducefile', help='File containing the reduce function source')
    parser.add_argument('-u', '--username', help='CouchDB username')
    parser.add_argument('-p', '--password', help='CouchDB password')
    parser.add_argument('-d', '--dbname', help='CouchDB database name', default='declarations')
    parser.add_argument('-e', '--endpoint', help='CouchDB endpoint', default='http://localhost:5984')
    parser.add_argument('-D', '--designdoc', help='CouchDB design doc name', default='default')
    parser.add_argument('-v', '--view', help='CouchDB view name')
    parser.add_argument('-l', '--language', help='Function language',
                        default='javascript',
                        choices=['javascript', 'coffeescript'])
    parser.add_argument('-V', '--verbose', help='Verbose logging', action='store_true', default=False)
    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    db_config = {
        'user': args.username,
        'password': args.password,
        'url': args.endpoint,
        'name': args.dbname,
        'design_doc': args.designdoc,
        'view': args.view
    }

    map_function_source, reduce_function_source = load_source(args.mapfile, args.reducefile)
    map_function_source, reduce_function_source = process_source(map_function_source,
                                                                 reduce_function_source, args.language)
    add_function(map_function_source, reduce_function_source, db_config)
