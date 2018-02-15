import argparse
from cloudant import couchdb
from load import get_all_uuids, logger


def export_all(db_config, state_filename):
    all_uuids = get_all_uuids(db_config, base_16=False)
    with open(state_filename, "w") as fp:
        fp.writelines("{}\n".format(x) for x in all_uuids)


if __name__ == '__main__':
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

    try:
        export_all(db_config, args.state)
    except KeyError:
        logger.error("DB config is wrong or DB doesn't exists")