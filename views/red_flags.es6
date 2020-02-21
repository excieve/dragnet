// Danger Zoooone
(doc) => {
    const nacp_doc = doc.nacp_orig;
    if (!nacp_doc.step_0 || nacp_doc.step_0.changesYear || !nacp_doc.step_0.declarationType)
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
    const exchange_rates_2017 = {
        "UAH": 1,
        "AUD": 21.849592,
        "THB": 0.860423,
        "BYN": 14.22782,
        "BGN": 17.126201,
        "KRW": 0.0262427,
        "HKD": 3.591078,
        "DKK": 4.498747,
        "USD": 28.067223,
        "EUR": 33.495424,
        "EGP": 1.583348,
        "JPY": 0.248593,
        "PLN": 8.011726,
        "INR": 0.4380033,
        "IRR": 0.000778,
        "CAD": 22.257575,
        "HRK": 4.459219,
        "MXN": 1.427329,
        "MDL": 1.641339,
        "ILS": 8.068853,
        "NZD": 19.871514,
        "NOK": 3.394692,
        "RUB": 0.48703,
        "RON": 7.20022,
        "IDR": 0.00206955,
        "SGD": 20.976593,
        "XDR": 39.875068,
        "KZT": 0.084716,
        "TRY": 7.368271,
        "HUF": 0.1079453,
        "GBP": 37.73367,
        "CZK": 1.306119,
        "SEK": 3.402209,
        "CHF": 28.618783,
        "CNY": 4.29423,
        "AZN": 15.973089,
        "DZD": 0.236304,
        "BRL": 8.321342,
        "AMD": 0.05607237,
        "AED": 7.393773,
        "VND": 0.0011955,
        "IQD": 0.023213,
        "GEL": 9.986338,
        "LBP": 0.0180259,
        "MYR": 6.63908,
        "MAD": 2.884563,
        "TWD": 0.905889,
        "PKR": 0.257866,
        "ZAR": 1.99531,
        "SAR": 7.241367,
        "RSD": 0.270046,
        "KGS": 0.389387,
        "TJS": 3.079034,
        "BDT": 0.331897,
        "TND": 10.959661,
        "TMT": 7.758814,
        "UZS": 0.003354,
        "QAR": 7.718486325,
        "UYU": 0.9742706225,
        "GHS": 6.202856283,
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
          income_presents_to_total_fraction_50 = 0.5,
          expenses_to_other_fraction = 3,
          liabilities_to_other_fraction = 2,
          total_cash_threshold = 5000000,
          total_cash_threshold_500k = 500000,
          lent_assets_threshold = 300000;

    // Flags
    let assets_to_income = false,
        expenses_to_inc_and_assets = false,
        liabilities_to_inc_and_assets = false,
        loan_shark = false,
        income_presents_to_total = false,
        income_presents_to_total_50 = false,
        income_has_prizes = false,
        jar_of_cash = false,
        jar_of_pocket_cash = false,
        garage_wo_car = false,
        has_luxury_cars = false,
        has_luxury_cars_v2 = false,
        vehicle_purch_no_cost = false,
        estate_purch_no_cost = false,
        house_no_land = false,
        estate_has_hidden_cost = false,
        corprights_has_foreign = false,
        has_foreign_bank_acc = false,
        hidden_in_family = false;
        has_aircraft_flag = false;
        has_major_real_estate = false;
        has_foreign_real_estate = false;
    // Helper values
    let total_income = 0.0,
        total_presents = 0.0,
        total_prizes = 0.0,
        total_expenses = 0.0,
        total_assets = 0.0,
        lent_assets = 0.0,
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
            if (ownership_types.indexOf(right.dnt_ownershipType_encoded) != -1) {
                return true;
            }
        }
        return false;
    };

    let convertCurrency = (amount, currency) => {
        let val = amount;
        if (currency && currency != 'UAH') {
            let exchange_table = exchange_rates_2017;
            if (nacp_doc.step_0.declarationYear1 == '2015')
                exchange_table = exchange_rates_2015;
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
            let has_real_estate = false;

            if (typeof(estate_doc) != 'object')
                continue;
            if (!isOwned(estate_doc))
                continue;

            switch (estate_doc.dnt_objectType_encoded) {
                case 'apt':
                case 'office':
                    has_real_estate = true
                    break;
                case 'garage':
                    has_garage = true;
                    break;
                case 'house':
                case 'dacha':
                    has_house = true;
                    has_real_estate = true;
                    break;
                case 'land':
                    has_land = true;
                    break;
                case 'other':
                    if (estate_doc.otherObjectType.toLowerCase().indexOf("будинок") != -1)
                        has_real_estate = true;
            }

            const owning_date = estate_doc.owningDate.split('.');
            if (owning_date.length == 3 && owning_date[2] == nacp_doc.step_0.declarationYear1 && !estate_doc.costDate)
                estate_purch_no_cost = true;

            if (estate_doc.dnt_costDate_hidden && estate_doc.dnt_costAssessment_hidden)
                estate_has_hidden_cost = true;

            if (String(estate_doc.person) in (nacp_doc.step_2 || {}) && (estate_doc.dnt_costDate_hidden || estate_doc.dnt_costAssessment_hidden))
                hidden_in_family = true;

            if (has_real_estate && estate_doc.totalArea > 300.)
                has_major_real_estate = true

            if (has_real_estate && String(estate_doc.country) != "1")
                has_foreign_real_estate = true
        }
    }
    if (nacp_doc.step_5) {
        for (let key in nacp_doc.step_5) {
            const valuables_doc = nacp_doc.step_5[key];
            if (typeof(valuables_doc) != 'object')
                continue;

            if (String(valuables_doc.person) in (nacp_doc.step_2 || {}) && valuables_doc.dnt_costDateUse_hidden)
                hidden_in_family = true;
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

            if (String(vehicle_doc.person) in (nacp_doc.step_2 || {}) && (vehicle_doc.dnt_costDate_hidden || vehicle_doc.dnt_graduationYear_hidden))
                hidden_in_family = true;

            if (vehicle_doc.dnt_objectType_encoded == "air_transport")
                has_aircraft_flag = true;

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
    if (nacp_doc.step_7) {
        for (let key in nacp_doc.step_7) {
            const securities_doc = nacp_doc.step_7[key];
            if (typeof(securities_doc) != 'object')
                continue;

            if (String(securities_doc.person) in (nacp_doc.step_2 || {}) && (securities_doc.dnt_amount_hidden || securities_doc.dnt_cost_hidden))
                hidden_in_family = true;
        }
    }
    if (nacp_doc.step_8) {
        for (let key in nacp_doc.step_8) {
            const corp_doc = nacp_doc.step_8[key];
            if (typeof(corp_doc) != 'object')
                continue;
            if (corp_doc.country != '1')
                corprights_has_foreign = true;
            if (String(corp_doc.person) in (nacp_doc.step_2 || {}) && corp_doc.dnt_cost_hidden)
                hidden_in_family = true;
        }
    }
    if (nacp_doc.step_11) {
        for (let key in nacp_doc.step_11) {
            const income_doc = nacp_doc.step_11[key];
            if (typeof(income_doc) != 'object')
                continue;

            if (String(income_doc.person) in (nacp_doc.step_2 || {}) && income_doc.dnt_sizeIncome_hidden)
                hidden_in_family = true;

            if (income_doc.sizeIncome === undefined)
                continue;
            if (present_types.indexOf(income_doc.dnt_objectType_encoded) != -1)
                total_presents += income_doc.sizeIncome;
            if (income_doc.dnt_objectType_encoded == 'prize')
                total_prizes += income_doc.sizeIncome;
            total_income += income_doc.sizeIncome;
        }
    }
    if (nacp_doc.step_12) {
        for (let key in nacp_doc.step_12) {
            const assets_doc = nacp_doc.step_12[key];
            if (typeof(assets_doc) != 'object')
                continue;

            if (assets_doc.dnt_objectType_encoded == 'bank' && assets_doc.dnt_is_foreign)
                has_foreign_bank_acc = true;

            if (String(assets_doc.person) in (nacp_doc.step_2 || {}) && assets_doc.dnt_sizeAssets_hidden)
                hidden_in_family = true;

            if (assets_doc.sizeAssets === undefined)
                continue;

            let val = convertCurrency(assets_doc.sizeAssets, assets_doc.assetsCurrency);
            if (val == null)
                continue;

            if (assets_doc.dnt_objectType_encoded == 'cash')
                total_cash += val;
            else if (assets_doc.dnt_objectType_encoded == 'lend')
                lent_assets += val;
            total_assets += val;
        }
    }
    if (nacp_doc.step_13) {
        for (let key in nacp_doc.step_13) {
            const liability_doc = nacp_doc.step_13[key];
            if (typeof(liability_doc) != 'object')
                continue;

            if (String(liability_doc.person) in (nacp_doc.step_2 || {}) && liability_doc.dnt_sizeObligation_hidden)
                hidden_in_family = true;

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

            if (String(expense_doc.person) in (nacp_doc.step_2 || {}) && expense_doc.dnt_costAmount_hidden)
                hidden_in_family = true;

            if (expense_doc.costAmount === undefined)
                continue;
            if (expense_doc.type != 1)
                continue;
            total_expenses += expense_doc.costAmount;
        }
    }

    if (total_income != 0) {
        assets_to_income = (total_assets / total_income) > assets_to_income_fraction;
        const presents_fraction = total_presents / total_income;
        income_presents_to_total = presents_fraction > income_presents_to_total_fraction;
        income_presents_to_total_50 = presents_fraction > income_presents_to_total_fraction_50;
    }
    const total_inc_and_assets = total_income + total_assets;
    if (total_inc_and_assets != 0) {
        expenses_to_inc_and_assets = (total_expenses / total_inc_and_assets) > expenses_to_other_fraction;
        liabilities_to_inc_and_assets = (total_liabilities / total_inc_and_assets) > liabilities_to_other_fraction;
    }
    jar_of_cash = total_cash > total_cash_threshold;
    jar_of_pocket_cash = total_cash > total_cash_threshold_500k;
    garage_wo_car = has_garage && !has_vehicle;
    house_no_land = has_house && !has_land;
    income_has_prizes = total_prizes > 0;
    loan_shark = lent_assets > lent_assets_threshold;

    emit(doc._id, [doc.doc_uuid, assets_to_income, income_presents_to_total, expenses_to_inc_and_assets,
                   liabilities_to_inc_and_assets, jar_of_cash, garage_wo_car, house_no_land, has_luxury_cars,
                   has_luxury_cars_v2, vehicle_purch_no_cost, estate_purch_no_cost, estate_has_hidden_cost,
                   corprights_has_foreign, has_foreign_bank_acc, income_has_prizes, loan_shark, jar_of_pocket_cash,
                   income_presents_to_total_50, hidden_in_family,
                   total_expenses, total_liabilities, total_cash, total_presents, has_aircraft_flag, 
                   has_major_real_estate, has_foreign_real_estate]);
}
