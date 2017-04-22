import logging
import argparse
import pandas

logging.basicConfig()
logger = logging.getLogger('dragnet.merge')
logger.setLevel(logging.INFO)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Merge multiple CSVs into one')
    parser.add_argument('files', help='CSV files. First one is base for others.', nargs='+')
    parser.add_argument('-o', '--output', help='Output file name', required=True)
    parser.add_argument('-f', '--field', help='Field to merge on', default='id')
    args = parser.parse_args()

    logger.info('Merging files: {}'.format(args.files))

    current_input = pandas.read_csv(args.files[0])
    logger.info('Base file: "{}"'.format(args.files[0]))
    for input_file in args.files[1:]:
        next_input = pandas.read_csv(input_file)
        # TODO: maybe modify to use other kinds of merges if needed in future
        current_input = current_input.merge(next_input, on=args.field, how='left', sort=False)
        logger.info('Merged file "{}"'.format(input_file))
    current_input.to_csv(args.output, index=False, na_rep='null')
    logger.info('Merged output wrote to file "{}"'.format(args.output))
