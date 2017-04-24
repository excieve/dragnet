import logging
import argparse
import pandas

logging.basicConfig()
logger = logging.getLogger('dragnet.merge')
logger.setLevel(logging.INFO)


NAN_REPLACEMENTS = {
    'types': {
        'int64': 0,
        'float64': 0.0,
        'bool': 'False',
        'object': ''
    },
    'columns': {
        'region': '!не визначено',
        # Somehow booleans don't get detected correctly
        'family': 'False',
        'incomes.has_hidden': 'False',
        'incomes.has_foreign': 'False',
        'assets.has_hidden': 'False',
        'assets.has_foreign': 'False',
        'estate.has_hidden': 'False',
        'estate.has_foreign': 'False',
        'vehicles.max_year': '!немає авто',
        'vehicles.has_hidden': 'False',
        'vehicles.any': 'False'
    }
}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Merge multiple CSVs into one')
    parser.add_argument('files', help='CSV files. First one is base for others.', nargs='+')
    parser.add_argument('-o', '--output', help='Output file name', required=True)
    parser.add_argument('-f', '--field', help='Field to merge on', default='id')
    parser.add_argument('-e', '--exclude', help='CSV file with IDs to exclude')
    args = parser.parse_args()

    logger.info('Merging files: {}'.format(args.files))

    current_input = pandas.read_csv(args.files[0])
    logger.info('Base file: "{}"'.format(args.files[0]))
    if args.exclude:
        logger.info('Excluding rows using file "{}"'.format(args.exclude))
        excludes = pandas.read_csv(args.exclude)
        current_input = current_input[~current_input[args.field].isin(excludes[args.field])]
    for input_file in args.files[1:]:
        next_input = pandas.read_csv(input_file)
        # TODO: maybe modify to use other kinds of merges if needed in future
        current_input = current_input.merge(next_input, on=args.field, how='left', sort=False)
        logger.info('Merged file "{}"'.format(input_file))
    # TODO: Make this configurable, think about generalised configs in fact
    logger.info('Replacing NaNs with predefined values')
    current_input = current_input[current_input['year'].isin([2015, 2016])]
    for column, dtype in current_input.dtypes.items():
        col_replacement = NAN_REPLACEMENTS['columns'].get(column, None)
        if not col_replacement:
            col_replacement = NAN_REPLACEMENTS['types'].get(dtype.name, None)
        current_input[column].fillna(col_replacement, inplace=True)

    current_input.to_csv(args.output, index=False, na_rep='null')
    logger.info('Merged output wrote to file "{}"'.format(args.output))
