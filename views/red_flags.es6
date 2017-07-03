// Danger Zoooone
(doc) => {
    const nacp_doc = doc.nacp_orig;
    if (nacp_doc.step_0 ||nacp_doc.step_0.changesYear || nacp_doc.step_0.declarationType)
        return;
    if (nacp_doc.step_0.declarationType != '1')
        return;

    // TODO: perhaps move this to a separate stored function with rates by year
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
    const luxury_car_names = [
        'acura', 'alfa romeo 4c', 'alfa romeo 4c spider', 'aston martin', 'audi a8', 'audi r8', 'audi tt', 'bentley',
        'bmw 6', 'bmw 7', 'bmw 8', 'cadillac', 'ferrari', 'fiat 124 spider', 'ford mustang', 'genesis g90',
        'honda s660', 'hyundai veloster', 'infiniti', 'jaguar', 'land rover', 'lexus', 'maserati', 'mazda mx 5', 'mclaren 570s',
        'mercedes amg gt', 'mercedes benz s class', 'mercedes benz sl class', 'mercedes benz slk class', 'nissan 370z',
        'nissan gt r', 'porsche', 'range rover', 'rolls royce', 'tesla model s', 'toyota 86', 'volkswagen phideon', 'акура',
        'альфа ромео 4с', 'альфа ромео 4с спайдер', 'астон мартин', 'астон мартін', 'ауди а8', 'ауди р8', 'ауди тт',
        'ауді а8', 'ауді р8', 'ауді тт', 'бентли', 'бентлі', 'бмв 6', 'бмв 7', 'бмв 8', 'дженезис г90', 'дженезіс г90',
        'инфинити', 'інфініті', 'кадилак', 'кадиллак', 'каділак', 'каділлак', 'лексус', 'лэнд ровер', 'ленд ровер',
        'мазда мх5', 'мазерати', 'мазераті', 'макларен 570с', 'мерседес амг гт', 'мерседес бенц с клас', 'мерседес бенц сл клас',
        'мерседес бенц слк клас', 'ниссан 370з', 'ниссан гт р', 'ніссан 370з', 'ніссан гт р', 'порш', 'порше',
        'рендж ровер', 'рейндж ровер', 'рэндж ровер', 'рэйндж ровер', 'роллс ройс', 'тесла модел с', 'тесла модель с',
        'тойота 86', 'ферари', 'ферарі', 'феррари', 'феррарі', 'фиат 124 спайдер', 'фіат 124 спайдер',
        'фольксваген фидеон', 'фольксваген фідеон', 'форд мустанг', 'хонда с660', 'хюндаи велостер', 'хюндаі велостер',
        'хюндай велостер', 'ягуар'
    ];
    const present_types = ['presentnomoney', 'presentmoney', 'charity', 'prize'],
          ownership_types = ['ownproperty', 'comproperty'];
    // Thresholds
    const assets_to_income_fraction = 10,
          income_presents_to_total_fraction = 0.75,
          expenses_to_other_fraction = 3,
          liabilities_to_other_fraction = 2,
          total_cash_threshold = 5000000;

    // Flags
    let assets_to_income = false,
        expenses_to_inc_and_assets = false,
        liabilities_to_inc_and_assets = false,
        income_presents_to_total = false,
        jar_of_cash = false,
        garage_wo_car = false,
        has_luxury_cars = false,
        has_luxury_cars_v2 = false,
        vehicle_purch_no_cost = false,
        estate_purch_no_cost = false,
        house_no_land = false;
    // Helper values
    let total_income = 0.0,
        total_presents = 0.0,
        total_expenses = 0.0,
        total_assets = 0.0,
        total_cash = 0.0,
        total_liabilities = 0.0,
        has_garage = false,
        has_vehicle = false,
        has_house = false,
        has_land = false;

    // TODO: preferably put these into separate common functions of their own
    let isOwned = (subdoc) => {
        if (!subdoc.rights)
            return false;
        for (let right_key in subdoc.rights) {
            const right = subdoc.rights[right_key];
            if (!right)
                continue;
            if (ownership_types.indexOf(right.ownershipType_encoded) != -1) {
                return true;
            }
        }
        return false;
    };

    let convertCurrency = (amount, currency) => {
        let val = amount;
        if (currency && currency != 'UAH') {
            let exchange_table = exchange_rates_2015;
            if (nacp_doc.step_0.declarationYear1 == '2016')
                exchange_table = exchange_rates_2016;
            if (!(currency in exchange_table))
                return null;
            val *= exchange_table[currency];
        }
        return val;
    };

    if (nacp_doc.step_3) {
        for (let key in nacp_doc.step_3) {
            const estate_doc = nacp_doc.step_3[key];
            if (typeof(estate_doc) != 'object')
                continue;
            if (!isOwned(estate_doc))
                continue;

            switch (estate_doc.objectType_encoded) {
                case 'garage':
                    has_garage = true;
                    break;
                case 'house':
                case 'dacha':
                    has_house = true;
                    break;
                case 'land':
                    has_land = true;
                    break;
            }

            const owning_date = estate_doc.owningDate.split('.');
            if (owning_date.length == 3 && owning_date[2] == nacp_doc.step_0.declarationYear1 && !estate_doc.costDate)
                estate_purch_no_cost = true;
        }
    }
    if (nacp_doc.step_6) {
        for (let key in nacp_doc.step_6) {
            const vehicle_doc = nacp_doc.step_6[key];
            if (typeof(vehicle_doc) != 'object')
                continue;
            if (!isOwned(vehicle_doc))
                continue;
            has_vehicle = true;

            const owning_date = vehicle_doc.owningDate.split('.');
            if (owning_date.length == 3 && owning_date[2] == nacp_doc.step_0.declarationYear1 && !vehicle_doc.costDate)
                vehicle_purch_no_cost = true;

            let full_name = '';
            if (vehicle_doc.brand)
                full_name += vehicle_doc.brand;
            if (vehicle_doc.model)
                full_name += ` ${vehicle_doc.model}`;
            if (full_name != '') {
                full_name = full_name.toLowerCase().replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g,' ').replace(/\s{2,}/g, ' ');
                for (let luxury_name of luxury_car_names) {
                    if (full_name.indexOf(luxury_name) != -1) {
                        has_luxury_cars = true;
                        if (!vehicle_doc.graduationYear || vehicle_doc.graduationYear >= 2011) {
                            has_luxury_cars_v2 = true;
                            break;
                        }
                    }
                }
            }
        }
    }
    if (nacp_doc.step_11) {
        for (let key in nacp_doc.step_11) {
            const income_doc = nacp_doc.step_11[key];
            if (typeof(income_doc) != 'object')
                continue;
            if (income_doc.sizeIncome === undefined)
                continue;
            if (present_types.indexOf(income_doc.objectType_encoded) != -1)
                total_presents += income_doc.sizeIncome;
            total_income += income_doc.sizeIncome;
        }
    }
    if (nacp_doc.step_12) {
        for (let key in nacp_doc.step_12) {
            const assets_doc = nacp_doc.step_12[key];
            if (typeof(assets_doc) != 'object')
                continue;
            if (assets_doc.sizeAssets === undefined)
                continue;

            let val = convertCurrency(assets_doc.sizeAssets, assets_doc.assetsCurrency);
            if (val == null)
                continue;

            if (assets_doc.objectType_encoded == 'cash')
                total_cash += val;
            total_assets += val;
        }
    }
    if (nacp_doc.step_13) {
        for (let key in nacp_doc.step_13) {
            const liability_doc = nacp_doc.step_13[key];
            if (typeof(liability_doc) != 'object')
                continue;
            if (liability_doc.sizeObligation === undefined)
                continue;

            let val = convertCurrency(liability_doc.sizeObligation, liability_doc.currency);
            if (val == null)
                continue;

            total_liabilities += val;
        }
    }
    if (nacp_doc.step_14) {
        for (let key in nacp_doc.step_14) {
            const expense_doc = nacp_doc.step_14[key];
            if (typeof(expense_doc) != 'object')
                continue;
            if (expense_doc.costAmount === undefined)
                continue;
            total_expenses += expense_doc.costAmount;
        }
    }

    if (total_income != 0) {
        assets_to_income = (total_assets / total_income) > assets_to_income_fraction;
        income_presents_to_total = (total_presents / total_income) > income_presents_to_total_fraction;
    }
    const total_inc_and_assets = total_income + total_assets;
    if (total_inc_and_assets != 0) {
        expenses_to_inc_and_assets = (total_expenses / total_inc_and_assets) > expenses_to_other_fraction;
        liabilities_to_inc_and_assets = (total_liabilities / total_inc_and_assets) > liabilities_to_other_fraction;
    }
    jar_of_cash = total_cash > total_cash_threshold;
    garage_wo_car = has_garage && !has_vehicle;
    house_no_land = has_house && !has_land;

    emit(doc._id, [assets_to_income, income_presents_to_total, expenses_to_inc_and_assets,
                   liabilities_to_inc_and_assets, jar_of_cash, garage_wo_car, house_no_land, has_luxury_cars,
                   has_luxury_cars_v2, vehicle_purch_no_cost, estate_purch_no_cost,
                   total_expenses, total_liabilities, total_cash, total_presents]);
}
