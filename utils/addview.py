import sys
import argparse
import logging
import subprocess
import time

from cloudant import couchdb

logger = logging.getLogger('dragnet.addview')


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


def load_source(mapfile_name, reducefile_name=None):
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
    new_language = language
    if language == 'coffeescript':
        logger.info('Compiling map function from CoffeeScript...')
        map_function_source = coffeescript(map_function_source)
        if not map_function_source:
            sys.exit(1)
        logger.info('Done.')
        if reduce_function_source:
            logger.info('Compiling reduce function from CoffeeScript...')
            reduce_function_source = coffeescript(reduce_function_source)
            if not reduce_function_source:
                sys.exit(1)
            logger.info('Done.')
        new_language = 'javascript'
    return map_function_source, reduce_function_source, new_language


def execute_view(couch, view):
    # Call the view in order to launch the indexing process.
    # This is fire and forget as it will most likely timeout and we're not interested in the result anyway.
    proc = subprocess.Popen(['curl', '-s', '{}?limit=1&reduce=false'.format(view.url)],
                            start_new_session=True, stdout=subprocess.DEVNULL)
    logger.info('Initiated the view query as pid {}.'.format(proc.pid))
    time.sleep(2)

    # Query CouchDB active tasks for the view's design doc while there's nothing left, then calculate average
    # Taken and adapted from https://gist.github.com/kevinjqiu/dd461b36a6f1d6d755d7a317d8f98b75#file-cps-py
    all_changes_per_sec = []
    all_changes_per_sec_one_task = []
    total_time = 0
    logger.info('Querying active tasks for the design document.')
    while True:
        response = couch.r_session.get('{}/_active_tasks'.format(couch.server_url))
        logger.debug(response.text)
        tasks = [
            task for task in response.json()
            if task.get('design_document') == view.design_doc['_id']
        ]
        if len(tasks) == 0:
            break

        task = tasks[0]
        started_on, updated_on = task['started_on'], task['updated_on']
        total_time = updated_on - started_on  # This will typically end up to be the last task's time, thus longest
        if total_time == 0:
            continue

        changes_per_sec = []
        for t in tasks:
            diff_t = float(t['updated_on'] - t['started_on'])
            if diff_t > 0:
                changes_per_sec.append(float(t.get('changes_done', 0)) / diff_t)
        all_changes_per_sec.append(sum(changes_per_sec))
        all_changes_per_sec_one_task.append(changes_per_sec[0])
        logger.info('c/s = {:.2f} ({} tasks), {:.2f} (one task); changes = {}'
                    .format(
                        sum(changes_per_sec), len(tasks),
                        changes_per_sec[0],
                        sum([t.get('changes_done', 0) for t in tasks])
                    ))
        time.sleep(1)

    if all_changes_per_sec:
        average_all = sum(all_changes_per_sec) / len(all_changes_per_sec)
        average_all_one_task = sum(all_changes_per_sec_one_task) / len(all_changes_per_sec_one_task)
        logger.info('average = {:.2f}c/s (all_tasks) {:.2f}c/s (one task)'.format(average_all, average_all_one_task))
        logger.info('total time = {}s'.format(total_time))
    else:
        logger.info('No active tasks (not indexing).')
    return all_changes_per_sec


def add_function(map_function_source, reduce_function_source, db_config, language, execute):
    with couchdb(db_config['user'], db_config['password'], url=db_config['url']) as couch:
        db = couch[db_config['name']]
        design_doc = db.get_design_document(db_config['design_doc'])
        logger.info('Working with design document {} from DB {}.'.format(design_doc['_id'], db.database_name))
        design_doc['language'] = language
        view = design_doc.get_view(db_config['view'])
        if view is None:
            logger.info('View {} does not exist, creating a new one.'.format(db_config['view']))
            design_doc.add_view(db_config['view'], map_function_source, reduce_function_source)
        else:
            logger.info('View {} exists, updating.'.format(view.view_name))
            design_doc.update_view(db_config['view'], map_function_source, reduce_function_source)
        logger.debug(design_doc.json())
        design_doc.save()
        logger.info('Design doc successfully saved.')
        logger.debug(design_doc.info())
        if execute:
            view = design_doc.get_view(db_config['view'])
            return execute_view(couch, view)


if __name__ == '__main__':
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)

    parser = argparse.ArgumentParser(description='Adds a MapReduce view to CouchDB database design doc')
    parser.add_argument('mapfile', help='File containing the map function source')
    parser.add_argument('-r', '--reducefile', help='File containing the reduce function source')
    parser.add_argument('-u', '--username', help='CouchDB username')
    parser.add_argument('-p', '--password', help='CouchDB password')
    parser.add_argument('-d', '--dbname', help='CouchDB database name', default='declarations')
    parser.add_argument('-e', '--endpoint', help='CouchDB endpoint', default='http://localhost:5984')
    parser.add_argument('-D', '--designdoc', help='CouchDB design doc name')
    parser.add_argument('-v', '--view', help='CouchDB view name')
    parser.add_argument('-l', '--language', help='Function language',
                        default='javascript',
                        choices=['javascript', 'coffeescript', 'chakra', 'python', 'pypy', 'erlang'])
    parser.add_argument('-V', '--verbose', help='Verbose logging', action='store_true', default=False)
    parser.add_argument('-b', '--benchmark', help='Measure performance metrics after adding the view',
                        action='store_true',
                        default=False)
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    db_config = {
        'user': args.username,
        'password': args.password,
        'url': args.endpoint,
        'name': args.dbname,
        'design_doc': args.designdoc,
        'view': args.view
    }

    map_function_source, reduce_function_source = load_source(args.mapfile, args.reducefile)
    map_function_source, reduce_function_source, language = process_source(map_function_source,
                                                                           reduce_function_source, args.language)
    add_function(map_function_source, reduce_function_source, db_config, language, args.benchmark)
