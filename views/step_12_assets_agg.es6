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

    let declarant_assets = 0.0,
        family_assets = 0.0,
        total_assets = 0.0,
        has_hidden = false,
        has_foreign = false;
    for (let key in doc.step_12) {
        const assets_doc = doc.step_12[key];
        if (typeof(assets_doc) != 'object')
            continue;
        // Sometimes there's just broken JSON
        if (assets_doc.sizeAssets === undefined)
            continue;
        if (assets_doc.is_foreign == true)
            has_foreign = true;
        if (assets_doc.sizeAssets_hidden) {
            has_hidden = true;
            continue;
        }

        let val = assets_doc.sizeAssets;
        if (assets_doc.assetsCurrency && assets_doc.assetsCurrency != 'UAH') {
            if (!(assets_doc.assetsCurrency in exchange_rates)) {
                log(`${assets_doc.assetsCurrency} currency code is not known`);
                continue;
            }
            val *= exchange_rates[assets_doc.assetsCurrency];
        }

        if (assets_doc.person == '1')
            declarant_assets += val;
        else if (String(assets_doc.person) in (doc.step_2 || {}))
            family_assets += val;
        total_assets += val;
    }

    emit([doc._id], [declarant_assets, family_assets, total_assets, has_hidden, has_foreign]);
}