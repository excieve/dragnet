def cmp_binning(left, right, zero_label, left_label, right_label):
    if not left:
        res = zero_label
    elif left < right:
        res = '2. {} < {}'.format(left_label, right_label)
    elif left < 2 * right:
        res = '3. {} < 2 * {}'.format(left_label, right_label)
    elif left < 5 * right:
        res = '4. {} < 5 * {}'.format(left_label, right_label)
    else:
        res = '5. {} >= 5 * {}'.format(left_label, right_label)
    return res


def percentage_binning(v, zero_label):
    if not v:
        res = zero_label
    elif v < 0.25:
        res = '2. До 25%'
    elif v < 0.75:
        res = '3. Від 25% до 75%'
    else:
        res = '4. Від 75%'
    return res


def postprocess_func(df):
    df['assets_incomes_ratio'] = df.apply(
        lambda r: cmp_binning(
            r['assets.total'], r['incomes.total'],
            zero_label='1. Немає активів взагалі',
            left_label='Активи',
            right_label='річний дохід'
        ), axis=1
    )
    df['liabilities_assets_and_incomes_ratio'] = df.apply(
        lambda r: cmp_binning(
            r['liabilities.total'], r['assets.total'] + r['incomes.total'],
            zero_label='1. Немає зобов’язань взагалі',
            left_label='Зобов’язання',
            right_label='(активи + річний дохід)'
        ), axis=1
    )
    df['expenses_assets_and_incomes_ratio'] = df.apply(
        lambda r: cmp_binning(
            r['expenses.total'], r['assets.total'] + r['incomes.total'],
            zero_label='1. Немає видатків взагалі',
            left_label='Видатки',
            right_label='(активи + річний дохід)'
        ), axis=1
    )

    df['assets.family_ratio_cat'] = df['assets.family_ratio'].apply(
        lambda v: percentage_binning(v, zero_label='1. Немає активів взагалі')
    )
    df['incomes.family_ratio_cat'] = df['incomes.family_ratio'].apply(
        lambda v: percentage_binning(v, zero_label='1. Немає доходів взагалі')
    )
    df['estate.family_land_ratio_cat'] = df['estate.family_land_ratio'].apply(
        lambda v: percentage_binning(v, zero_label='1. Немає землі взагалі')
    )
    df['estate.family_other_ratio_cat'] = df['estate.family_other_ratio'].apply(
        lambda v: percentage_binning(v, zero_label='1. Немає нерухомості взагалі')
    )
    return df
