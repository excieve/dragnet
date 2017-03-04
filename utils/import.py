import logging
import json
import argparse
from itertools import zip_longest
from functools import partial
from multiprocessing import Pool, log_to_stderr
from time import process_time

from cloudant import couchdb


logger = log_to_stderr()
logger.setLevel(logging.INFO)


def import_batch(docs, db_config):
    """Bulk import a batch of ElasticSearch-like documents into CouchDB"""
    t1 = process_time()
    docs_objects = []
    for d in docs:
        if d:
            doc_object = json.loads(d)
            source = doc_object['_source']['nacp_orig']
            source.update({'_id': doc_object['_id']})
            docs_objects.append(source)

    with couchdb(db_config['user'], db_config['password'], url=db_config['url']) as couch:
        db = couch[db_config['name']]
        db.bulk_docs(docs_objects)
    t2 = process_time()
    return len(docs_objects), t2 - t1


def grouper(iterable, n, fillvalue=None):
    """Collect data into fixed-length chunks or blocks"""
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def import_all(docs_file, db_config, concurrency, chunks_per_process):
    total_docs, total_time = 0, 0
    with open(docs_file, 'r', encoding='utf-8') as f:
        with Pool(concurrency) as pool:
            # Lazily consume batches of `chunks_per_process` for every process in the pool of `concurrency`
            results = pool.imap(partial(import_batch, db_config=db_config),
                                grouper(f, chunks_per_process))
            for i, result in enumerate(results):
                num_docs, time_spent = result
                total_docs += num_docs
                total_time += time_spent
                logger.info(
                    'Batch #{} finished importing {} documents in {:.2f}s with the speed of {:.2f}docs/s'
                    .format(i, num_docs, time_spent, float(num_docs) / float(time_spent))
                )
    logger.info(
        'Total imported {} documents in {:.2f}s with the speed of {:.2f}docs/s'
        .format(total_docs, total_time, float(total_docs) / float(total_time))
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Import documents from ElasticSearch-like dump to CouchDB')
    parser.add_argument('docs_file', help='Documents file')
    parser.add_argument('-u', '--username', help='CouchDB username')
    parser.add_argument('-p', '--password', help='CouchDB password')
    parser.add_argument('-d', '--dbname', help='CouchDB database name', default='declarations')
    parser.add_argument('-e', '--endpoint', help='CouchDB endpoint', default='http://localhost:5984')
    parser.add_argument('-c', '--concurrency', help='Number of processes to spawn', type=int, default=8)
    parser.add_argument('-C', '--chunks', help='Number of chunks to run in a batch', type=int, default=1500)
    parser.add_argument('-P', '--purge', help='Purge the DB before importing', action='store_true', default=False)
    args = parser.parse_args()

    db_config = {
        'user': args.username,
        'password': args.password,
        'url': args.endpoint,
        'name': args.dbname
    }

    # Ensure our DB exists before actually importing
    with couchdb(db_config['user'], db_config['password'], url=db_config['url']) as couch:
        try:
            db = couch[args.dbname]
            if args.purge:
                db.delete()
                logger.info('Database {} purged.'.format(args.dbname))
        except KeyError:
            pass
        db = couch.create_database(args.dbname, throw_on_exists=False)
        if db.exists():
            logger.info('Database {} created or already exists'.format(args.dbname))

    import_all(args.docs_file, db_config, args.concurrency, args.chunks)
