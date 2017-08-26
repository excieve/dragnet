(doc) => {
    const nacp_doc = doc.nacp_orig;
    if (!nacp_doc.step_0 || nacp_doc.step_0.changesYear || !nacp_doc.step_0.declarationType || !nacp_doc.step_12)
        return;

    const exchange_rates_2015 = {
        "UAH": 1,
        "AED": 6.535141617,
        "AMD": 0.04961378,
        "AUD": 17.49374800,
        "AZN": 15.39096300,
        "BGN": 13.40787800,
        "BRL": 6.21135300,
        "BYR": 0.00129000,
        "CAD": 17.28503600,
        "CHF": 24.24924100,
        "CLP": 0.03397600,
        "CNY": 3.69808600,
        "CZK": 0.97018500,
        "DKK": 3.51398700,
        "EGP": 3.06521900,
        "EUR": 26.22312900,
        "GBP": 35.53317600,
        "GEL": 10.02157400,
        "HKD": 3.09654900,
        "HRK": 3.43369500,
        "HUF": 0.08373980,
        "ILS": 6.16001900,
        "INR": 0.36240930,
        "IQD": 0.02191800,
        "IRR": 0.00080440,
        "ISK": 0.18541900,
        "JPY": 0.19917310,
        "KGS": 0.31621700,
        "KRW": 0.02041040,
        "KWD": 79.13177400,
        "KZT": 0.07070000,
        "LBP": 0.01593990,
        "LYD": 17.31899800,
        "MDL": 1.21991200,
        "MNT": 0.01206064,
        "MXN": 1.391787,
        "NOK": 2.727031,
        "NZD": 16.431561,
        "PEN": 7.05902,
        "PKR": 0.229014,
        "PLN": 6.1847,
        "RON": 5.789281,
        "RUB": 0.32931,
        "SAR": 6.403251,
        "SEK": 2.854125,
        "SGD": 16.973998,
        "SYP": 0.109243,
        "TJS": 3.438343,
        "TMT": 6.857333,
        "TRY": 8.236683,
        "TWD": 0.731393,
        "USD": 24.000667,
        "UZS": 0.008541,
        "VND": 0.00106812,
        "XDR": 33.285487,
        "XOF": 0.0399625,
        "QAR": 6.589863138,
        "UYU": 0.8023422978,
        "GHS": 6.291054834
    }
    const exchange_rates_2016 = {
        "UAH": 1,
        "AED": 7.403708,
        "AMD": 0.05622011,
        "AUD": 19.595039,
        "AZN": 15.395118,
        "BDT": 0.344537,
        "BGN": 14.53247,
        "BRL": 8.329456,
        "BYN": 13.88351,
        "CAD": 20.080969,
        "CHF": 26.528471,
        "CNY": 3.909251,
        "CZK": 1.051871,
        "DKK": 3.823429,
        "DZD": 0.245581,
        "EGP": 1.500417,
        "EUR": 28.422604,
        "GBP": 33.320755,
        "GEL": 10.236751,
        "HKD": 3.505674,
        "HRK": 3.759952,
        "HUF": 0.0916592,
        "IDR": 0.00201975,
        "ILS": 7.06573,
        "INR": 0.3997834,
        "IQD": 0.023043,
        "IRR": 0.0008398,
        "JPY": 0.2328958,
        "KGS": 0.391796,
        "KRW": 0.0224818,
        "KZT": 0.081586,
        "LBP": 0.018061,
        "MAD": 2.671008,
        "MDL": 1.360808,
        "MXN": 1.31386,
        "MYR": 6.063359,
        "NOK": 3.131691,
        "NZD": 18.898008,
        "PKR": 0.259455,
        "PLN": 6.439048,
        "RON": 6.263935,
        "RSD": 0.230061,
        "RUB": 0.45113,
        "SAR": 7.249156,
        "SEK": 2.973542,
        "SGD": 18.753368,
        "THB": 0.756564,
        "TJS": 3.451975,
        "TMT": 7.768817,
        "TND": 11.610102,
        "TRY": 7.697179,
        "TWD": 0.838706,
        "USD": 27.190858,
        "UZS": 0.008451,
        "VND": 0.00119415,
        "XDR": 36.438125,
        "ZAR": 1.988679,
        "QAR": 7.468241058,
        "UYU": 0.9285678007,
        "GHS": 6.359669778
    }

    let declarant_assets = 0.0,
        family_assets = 0.0,
        total_assets = 0.0,
        has_hidden = false,
        has_foreign = false;
    for (let key in nacp_doc.step_12) {
        const assets_doc = nacp_doc.step_12[key];
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
            let exchange_table = exchange_rates_2015;
            if (nacp_doc.step_0.declarationYear1 == '2016')
                exchange_table = exchange_rates_2016;
            if (!(assets_doc.assetsCurrency in exchange_table)) {
                log(`${assets_doc.assetsCurrency} currency code is not known`);
                continue;
            }
            val *= exchange_table[assets_doc.assetsCurrency];
        }

        if (assets_doc.person == '1')
            declarant_assets += val;
        else if (String(assets_doc.person) in (nacp_doc.step_2 || {}))
            family_assets += val;
        total_assets += val;
    }

    emit(doc._id, [doc.doc_uuid, declarant_assets, family_assets, total_assets, has_hidden, has_foreign]);
}