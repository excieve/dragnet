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

    df = pandas.read_csv(args.files[0])
    logger.info('Base file: "{}"'.format(args.files[0]))
    if args.exclude:
        logger.info('Excluding rows using file "{}"'.format(args.exclude))
        excludes = pandas.read_csv(args.exclude)
        df = df[~df[args.field].isin(excludes[args.field])]
    for input_file in args.files[1:]:
        next_input = pandas.read_csv(input_file)
        # TODO: maybe modify to use other kinds of merges if needed in future
        df = df.merge(next_input, on=args.field, how='left', sort=False)
        logger.info('Merged file "{}"'.format(input_file))
    # TODO: Make this configurable, think about generalised configs in fact
    logger.info('Filtering out irrelevant years')
    df = df[df['year'].isin([2015, 2016])]
    logger.info('Replacing NaNs with predefined values')
    for column, dtype in df.dtypes.items():
        col_replacement = NAN_REPLACEMENTS['columns'].get(column, None)
        if not col_replacement:
            col_replacement = NAN_REPLACEMENTS['types'].get(dtype.name, None)
        df[column].fillna(col_replacement, inplace=True)

    # TODO: Generalise outliers
    df['outlier'] = False
    q1 = ((df['incomes.total'] > 100000000) | (df['estate.total_other'] > 5000))\
        & (df['name_post'].str.contains('депутат', case=False))
    q2 = (df['estate.total_land'] > 20000000)
    q3 = (df['estate.total_other'] > 20000)
    q4 = (df['vehicles.total_cost'] > 10000000) & (df['lux_cars_flag'] == False)  # noqa
    q5 = (df['id'] == "nacp_43c9b02f-4752-47ec-a784-f9a39d7a5ab3")
    excl = (~df['id'].isin([
        'nacp_08a63d8b-2db4-4ef0-8b8b-396e0cd9f495',
        'nacp_7762d918-fe93-4285-8703-7fbe18312634',
        'nacp_50a32d11-ebfa-4466-9bde-2f049cb00574']))
    df.loc[(q1 | q2 | q3 | q4 | q5) & excl, 'outlier'] = True

    df.to_csv(args.output, index=False, na_rep='null')
    logger.info('Merged output wrote to file "{}"'.format(args.output))
