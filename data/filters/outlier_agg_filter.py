def postprocess_func(df):
    df['outlier'] = False

    q1 = ((df['incomes.total'] > 100000000) | (df['estate.total_other'] > 5000))\
        & (~df['name_post'].str.contains('депутат', case=False))
    q2 = (df['estate.total_land'] > 20000000)
    q3 = (df['estate.total_other'] > 20000)
    q4 = (df['vehicles.total_cost'] > 10000000) & (df['lux_cars_flag'] == False)  # noqa
    q5 = (df['id'] == 'nacp_43c9b02f-4752-47ec-a784-f9a39d7a5ab3')

    q6 = ((df['assets.total'] > 1000000000))\
        & (~df['name_post'].str.contains('депутат', case=False))

    excl = (~df['id'].isin([
        'nacp_08a63d8b-2db4-4ef0-8b8b-396e0cd9f495',
        'nacp_7762d918-fe93-4285-8703-7fbe18312634',
        'nacp_50a32d11-ebfa-4466-9bde-2f049cb00574']))
    df.loc[(q1 | q2 | q3 | q4 | q5 | q6) & excl, 'outlier'] = True

    return df
