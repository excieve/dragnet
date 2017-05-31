import logging
import argparse
import pandas

logger = logging.getLogger('dragnet.merge')


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


def default_outlier_filters(df):
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
    return (q1 | q2 | q3 | q4 | q5) & excl


def merge_csv(filename, inputs, on_field, nan_replacements=None, outlier_filters=None, only_years=None):
    logger.info('Merging files: {}'.format(inputs))

    df = pandas.read_csv(inputs[0])
    logger.info('Base file: "{}"'.format(inputs[0]))
    for input_file in inputs[1:]:
        next_input = pandas.read_csv(input_file)
        # TODO: maybe modify to use other kinds of merges if needed in future
        df = df.merge(next_input, on=on_field, how='left', sort=False)
        logger.info('Merged file "{}"'.format(input_file))

    if only_years:
        logger.info('Filtering out irrelevant years')
        df = df[df['year'].isin(only_years)]

    if nan_replacements:
        logger.info('Replacing NaNs with predefined values')
        for column, dtype in df.dtypes.items():
            col_replacement = nan_replacements['columns'].get(column, None)
            if not col_replacement:
                col_replacement = nan_replacements['types'].get(dtype.name, None)
            df[column].fillna(col_replacement, inplace=True)

    if outlier_filters:
        df['outlier'] = False
        df.loc[outlier_filters(df), 'outlier'] = True

    df.to_csv(filename, index=False, na_rep='null')
    logger.info('Merged output wrote to file "{}"'.format(filename))


if __name__ == '__main__':
    logging.basicConfig()
    logger.setLevel(logging.INFO)

    parser = argparse.ArgumentParser(description='Merge multiple CSVs into one')
    parser.add_argument('files', help='CSV files. First one is base for others.', nargs='+')
    parser.add_argument('-o', '--output', help='Output file name', required=True)
    parser.add_argument('-f', '--field', help='Field to merge on', default='id')
    args = parser.parse_args()

    merge_csv(args.output, args.files, args.field, NAN_REPLACEMENTS, default_outlier_filters, only_years=[2015, 2016])
