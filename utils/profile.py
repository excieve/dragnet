import logging
import argparse
import json

logging.basicConfig()
logger = logging.getLogger('dragnet.profile')
logger.setLevel(logging.INFO)


def runner(profile, input_filename):
    pass


def exporter(profile, datadir):
    pass


def merger(profile, datadir):
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Execute a Dragnet profile')
    parser.add_argument('action', help='Action to execute (use "all" to sequentially perform every action)',
                        choices=['all', 'runner', 'exporter', 'merger'])
    parser.add_argument('profile', help='Profile to execute')
    parser.add_argument('--input', '-f', help='Input data file')
    parser.add_argument('--datadir', '-d', help='Data directory', default='data')
    args = parser.parse_args()

    with open(args.profile, 'r', encoding='utf-8') as fp:
        profile = json.load(fp)
    if args.action in ('all', 'runner'):
        runner(profile, args.input)
    if args.action in ('all', 'exporter'):
        exporter(profile, args.datadir)
    if args.action in ('all', 'merger'):
        merger(profile, args.datadir)
