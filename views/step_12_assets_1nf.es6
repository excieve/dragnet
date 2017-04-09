(doc) => {
    if (!doc.step_0 || doc.step_0.changesYear || !doc.step_0.declarationType || !doc.step_12)
        return;
    if (doc.step_0.declarationType != '1')
        return;

    const exchange_rates = {
        "UAH": 1,
        "AUD": 17.49374800,
        "BYR": 0.00129000,
        "DKK": 3.51398700,
        "USD": 24.00066700,
        "EUR": 26.22312900,
        "JPY": 0.19917310,
        "PLN": 6.18470000,
        "ISK": 0.18541900,
        "CAD": 17.28503600,
        "MDL": 1.21991200,
        "NOK": 2.72703100,
        "RUB": 0.32931000,
        "SGD": 16.97399800,
        "XDR": 33.28548700,
        "KZT": 0.07070000,
        "TRY": 8.23668300,
        "HUF": 0.08373980,
        "GBP": 35.53317600,
        "CZK": 0.97018500,
        "SEK": 2.85412500,
        "CHF": 24.24924100,
        "CNY": 3.69808600,
        "QAR": 6.60066007,
        "BGN": 12.95361500,
        "GEL": 9.95679600,
        "HKD": 3.09001000,
        "SAR": 6.38190200,
        "AED": 7.32064422,
        "UYU": 0.94813691,
        "HRK": 3.83860000,
        "GHS": 5.85950000,
    }

    let result_dict = {},
        person_key = ''
        curr_key = 'UAH'
        val = 0.0;
    for (let key in doc.step_12) {
        const assets_doc = doc.step_12[key];
        if (typeof(assets_doc) != 'object')
            continue;
        if (assets_doc.sizeAssets == 'NaN')
            continue;

        if (assets_doc.person == '1')
            person_key = 'd';  // D is for Declarant
        else if (String(assets_doc.person) in (doc.step_2 || {}))
            person_key = 'f';  // F is for Family
        else {
            person_key = 'u';  // U is for fUcked Up
        }

        val = assets_doc.sizeAssets;
        if (assets_doc.assetsCurrency && assets_doc.assetsCurrency != 'UAH') {
            curr_key = 'OTH';
            if (!(assets_doc.assetsCurrency in exchange_rates)) {
                log(`${assets_doc.assetsCurrency} currency code is not known`);
                continue;
            }

            val *= exchange_rates[assets_doc.assetsCurrency];
        }

        const result_key = `${person_key}.${assets_doc.objectType_encoded}.${assets_doc.is_foreign}.${curr_key}`;
        if (result_key in result_dict)
            result_dict[result_key] += val;
        else
            result_dict[result_key] = val;
    }

    for (let key in result_dict)
        emit([doc._id].concat(key.split('.')), result_dict[key]);
}