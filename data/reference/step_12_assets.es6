// let f = (doc) => {
(doc) => {
    const assetsMapping = {
        "кошти, розміщені на банківських рахунках": "bank",
        "готівкові кошти": "cash",
        "внески до кредитних спілок та інших небанківських фінансових установ": "credit_union",
        "кошти, позичені третім особам": "lend",
        "активи у дорогоцінних (банківських) металах": "metals",
        "інше": "other"
    };

    const exchangeRates = {
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

    const personValues = ["d", "f", "u"],
          geoSourceValues = ["ukr", "abr"],
          currencyValues = ["UAH", "OTH"],
          abroadSources = [
            "іноземний громадянин",
            "юридична особа, зареєстрована за кордоном"
    ];

    if (!doc.step_0 || doc.step_0.changesYear || !doc.step_0.declarationType)
        return;

    if (doc.step_0.declarationType != '1')
        return;

    let result_dict = {},
        family = [],
        person_key = "",
        source_key = "",
        geosource_key = "",
        curr;

    for (let person in personValues) {
        result_dict[`assets.hidden.${personValues[person]}`] = 0.0;
        for (let geo_src in geoSourceValues)
            for (let src in assetsMapping)
                for (let curr in currencyValues)
                    result_dict[`assets.sum.${personValues[person]}.${geoSourceValues[geo_src]}.${assetsMapping[src]}.${currencyValues[curr]}`] = 0.0;
    }


    if (doc.step_2) {
        family = Object.keys(doc.step_2);
    }

    if (doc.step_12) {
        for (let key in doc.step_12) {
            const assetsDoc = doc.step_12[key];
            if (typeof(assetsDoc) != 'object')
                continue;

            if (assetsDoc.person == '1')
                person_key = "d";  // D is for Declarant
            else if (family.indexOf(String(assetsDoc.person)) != -1)
                person_key = "f";  // F is for Family
            else {
                person_key = "u";  // U is for fUcked Up
            }

            if (assetsDoc.objectType.toLowerCase() in assetsMapping)
                source_key = assetsMapping[assetsDoc.objectType.toLowerCase()]
            else
                source_key = "other";

            if (abroadSources.indexOf(assetsDoc.organization_type.toLowerCase()) != -1)
                geosource_key = "abr";
            else
                geosource_key = "ukr";

            let val = Number.parseInt(assetsDoc.sizeAssets);

            if (assetsDoc.assetsCurrency == "UAH") {
                curr = "UAH"
            }else {
                curr = "OTH"
                val *= exchangeRates[assetsDoc.assetsCurrency]
            }

            if (!Number.isNaN(val))
                result_dict[`assets.sum.${person_key}.${geosource_key}.${source_key}.${curr}`] += val;
            else
                result_dict[`assets.hidden.${person_key}`] = 1;
        };
    }

    emit(doc._id, result_dict);
    // return result_dict;
}

// let json_data = require('../../test_assets/poroshenko_jr.json')
// console.log(f(json_data["data"]))

// json_data = require('../../test_assets/poroshenko.json')
// console.log(f(json_data["data"]))

// json_data = require('../../test_assets/derkatch.json')
// console.log(f(json_data["data"]))
