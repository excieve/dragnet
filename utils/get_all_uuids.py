import logging
import argparse
from multiprocessing import log_to_stderr

from cloudant import couchdb

from load import get_all_uuids

logger = log_to_stderr()

def export_all(db_config, state_filename):
    all_uuids = get_all_uuids(db_config, base_16=False)
    with open(state_filename, "w") as fp:
        fp.writelines("{}\n".format(x) for x in all_uuids)


if __name__ == '__main__':
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)

    parser = argparse.ArgumentParser(description='Get all uuids of documents from couchdb to text file')
    parser.add_argument('-u', '--username', help='CouchDB username')
    parser.add_argument('-p', '--password', help='CouchDB password')
    parser.add_argument('-d', '--dbname', help='CouchDB database name', default='declarations')
    parser.add_argument('-e', '--endpoint', help='CouchDB endpoint', default='http://localhost:5984')
    parser.add_argument('state', help='Save all UUIDs to a provided file')
    args = parser.parse_args()

    db_config = {
        'user': args.username,
        'password': args.password,
        'url': args.endpoint,
        'name': args.dbname
    }

    # Ensure our DB exists before actually importing
    with couchdb(db_config['user'], db_config['password'], url=db_config['url']) as couch:
        db = couch[args.dbname]
        db = couch.create_database(args.dbname, throw_on_exists=False)
        if db.exists():
            logger.info('Database {} created or already exists'.format(args.dbname))

    export_all(db_config, args.state)
