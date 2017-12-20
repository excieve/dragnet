import logging
import argparse
import pandas

logger = logging.getLogger('dragnet.merge')


def merge_csv(filename, inputs, on_field, nan_replacements=None, postprocess_funcs=None, only_years=None):
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

    if df.empty:
        logger.warning('Resulting CSV is empty')
        return

    if nan_replacements:
        logger.info('Replacing NaNs with predefined values')
        for column, dtype in df.dtypes.items():
            col_replacement = nan_replacements['columns'].get(column, None)
            if not col_replacement:
                col_replacement = nan_replacements['types'].get(dtype.name, None)
            df[column].fillna(col_replacement, inplace=True)

    if postprocess_funcs:
        for pp_func in postprocess_funcs:
            logger.info('Applying post-processing function')
            df = pp_func(df)

    logger.info('Exporting to CSV')
    df.to_csv(filename, index=False, na_rep='null')
    logger.info('Merged output wrote to file "{}"'.format(filename))


if __name__ == '__main__':
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)

    parser = argparse.ArgumentParser(description='Merge multiple CSVs into one')
    parser.add_argument('files', help='CSV files. First one is base for others.', nargs='+')
    parser.add_argument('-o', '--output', help='Output file name', required=True)
    parser.add_argument('-f', '--field', help='Field to merge on', default='id')
    args = parser.parse_args()

    merge_csv(args.output, args.files, args.field)
