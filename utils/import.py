import logging
import argparse
import glob2
import os.path

from itertools import zip_longest
from functools import partial
from multiprocessing import Pool, log_to_stderr
from time import perf_counter
from uuid import UUID

from cloudant import couchdb


from nacp_parser import NacpDeclarationParser
from nacp_normaliser import preprocess_nacp_doc


logger = log_to_stderr()


def import_batch(docs, db_config):
    """Bulk import a batch of ElasticSearch-like documents into CouchDB"""
    t1 = perf_counter()
    docs_objects = []
    for doc_file in docs:
        if not doc_file:
            continue
        doc_object = NacpDeclarationParser.parse(doc_file)
        if doc_object:
            source = doc_object
            source.update({
                # Convert string UUID to int for less storage and much faster sorting as CouchDB doc ID.
                # String representation still persisted in the doc body.
                '_id': str(UUID(doc_object['doc_uuid'].replace('nacp_', '')).int),
            })
            docs_objects.append(preprocess_nacp_doc(source))
    imported = 0
    with couchdb(db_config['user'], db_config['password'], url=db_config['url']) as couch:
        db = couch[db_config['name']]
        # When trying to bulk insert an existing document without providing a new revision ID CouchDB will
        # throw a conflict error, we'll use this to only insert new stuff without explicit existence checks.
        imported_docs = list(filter(lambda x: x.get('error') is None, db.bulk_docs(docs_objects)))
        imported += len(imported_docs)
    t2 = perf_counter()
    return len(docs_objects), imported, t2 - t1


def grouper(iterable, n, fillvalue=None):
    """Collect data into fixed-length chunks or blocks"""
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def import_all(docs_dir, db_config, concurrency, chunks_per_process):
    total_imported_docs, rates = 0, []
    jsons = glob2.iglob(os.path.join(docs_dir, "**/*.json"))
    with Pool(concurrency) as pool:
        # Lazily consume batches of `chunks_per_process` for every process in the pool of `concurrency`
        results = pool.imap(partial(import_batch, db_config=db_config),
                            grouper(jsons, chunks_per_process))
        for i, result in enumerate(results):
            num_docs, imported_docs, time_spent = result
            total_imported_docs += imported_docs
            rate = float(num_docs) / float(time_spent)
            rates.append(rate)
            logger.info(
                'Batch #{} finished importing {} new documents in {:.2f}s with the rate of {:.2f}docs/s'
                .format(i, imported_docs, time_spent, rate)
            )
    logger.info(
        'Total imported {} new documents with the avg rate of {:.2f}docs/s across all processes'
        .format(total_imported_docs, sum(rates) / float(len(rates)) * concurrency)
    )


if __name__ == '__main__':
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)

    parser = argparse.ArgumentParser(description='Import documents to CouchDB')
    parser.add_argument('docs_dir', help='Documents directory')
    parser.add_argument('-u', '--username', help='CouchDB username')
    parser.add_argument('-p', '--password', help='CouchDB password')
    parser.add_argument('-d', '--dbname', help='CouchDB database name', default='declarations')
    parser.add_argument('-e', '--endpoint', help='CouchDB endpoint', default='http://localhost:5984')
    parser.add_argument('-c', '--concurrency', help='Number of processes to spawn', type=int, default=8)
    parser.add_argument('-C', '--chunks', help='Number of chunks to run in a batch', type=int, default=200)
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

    import_all(args.docs_dir, db_config, args.concurrency, args.chunks)
