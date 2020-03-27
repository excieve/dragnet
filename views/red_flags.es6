// Danger Zoooone
(doc) => {
    const nacp_doc = doc.nacp_orig;
    if (!nacp_doc.step_0 || nacp_doc.step_0.changesYear || !nacp_doc.step_0.declarationType)
        return;

    const common_bank_names = [
        "твбв",
        "ощадбанк",
        "приватбанк",
        "аваль",
        "райффайзен",
        "абанк",
        "агріколь",
        "укрсиббанк",
        "альфабанк",
        "пумб",
        "укргазбанк",
        "мегабанк",
        "акордбанк",
        "сбербанк",
        "таскомбанк",
        "кредобанк",
        "індустріалбанк",
        "укрексімбанк",
        "радабанк",
        "укркомунбанк",
        "укрбудінвестбанк",
        "правексбанк",
        "правекс",
        "прокредит",
        "метабанк",
        "комінвестбанк",
        "форвард",
        "дельта-банк",
        "дельтабанк",
        "укрсоцбанк",
        "дельта банк",
    ];

    const common_bank_codes = [
        "19358916",
        "22808607",
        "21420657",
        "23321095",
        "9338500",
        "19369239",
        "25292831",
        "20021814",
        "39025",
        "26547581",
        "9336500",
        "20026838",
        "9304612",
        "9805171",
        "14361032",
        "13550848",
        "21665382",
        "14263173",
        "19361746",
        "9620081",
        "9303328",
        "33695095",
        "35371070",
        "38781707",
        "19364130",
        "20935649",
        "33294890",
        "34693790",
        "19358767",
        "19361982",
        "24905013",
        "20953647",
        "35574578",
        "20077200",
        "33972230",
        "20966466",
        "36002395",
        "36061927",
        "35917889",
        "21595828",
        "9311380",
        "19357443",
        "38322199",
        "9351600",
        "9807862",
        "9323408",
        "20569558",
        "19364584",
        "38514375",
        "19233095",
        "21329000",
        "20050951",
        "14282829",
        "21574573",
        "20679755",
        "21955111",
        "19361427",
        "37716841",
        "38619024",
        "2068095",
        "36520434",
        "36335426",
        "20929956",
        "19020301",
        "20510134",
        "35863708",
        "9809192",
        "16328435",
        "26253000",
        "26410155",
        "20496061",
        "19358282",
        "23494105",
        "22932856",
        "14360920",
        "21554560",
        "9333401",
        "26410346",
        "21568696",
        "21322127",
        "20935846",
        "26549700",
        "22868414",
        "21673424",
        "14359845",
        "21570492",
        "9305480",
        "21666051",
        "9356307",
        "14349442",
        "26333064",
        "20025456",
        "37987811",
        "13857564",
        "19357489",
        "20023463",
        "24425738",
        "38061253",
        "22869483",
        "1904694",
        "38870739",
        "34353904",
        "20015529",
        "14305909",
        "20846070",
        "19159542",
        "36470620",
        "20685262",
        "13881479",
        "14351016",
        "20305925",
        "24262992",
        "9328601",
        "35345213",
        "20280450",
        "19357325",
        "20041917",
        "26475516",
        "9806443",
        "13486837",
        "19358454",
        "26364113",
        "33308489",
        "23024763",
        "21685485",
        "19019775",
        "24363820",
        "9315357",
        "33881201",
        "37515069",
        "23307646",
        "38770082",
        "37176171",
        "19364259",
        "9801546",
        "19017842",
        "21536532",
        "20058668",
        "14360721",
        "14359319",
        "21734522",
        "34186061",
        "19359784",
        "21684161",
        "20971504",
        "34819265",
        "9804355",
        "9334702",
        "9804119",
        "23362711",
        "20748213",
        "19358201",
        "34576883",
        "21593719",
        "13641864",
        "39002",
        "19357762",
        "14070197",
        "19358796",
        "19356840",
        "23876031",
        "19358632",
        "9807750",
        "9806354",
        "9325703",
        "19388768",
        "9353504",
        "19358419",
        "19361386",
        "20053145",
        "34575675",
        "36482677",
        "21684818",
        "9807595",
        "19454139",
        "14366762",
        "33299878",
        "20042809",
        "34514392",
        "39037656",
        "38377143",
        "39019",
        "2073574",
        "20057663",
        "9806437",
        "26444836",
        "23478833",
        "9322299",
        "24191588",
        "21063524",
        "14358604",
        "20034231",
        "5839888",
        "23494714",
        "14352406",
        "20401758",
        "25571287",
        "21296105",
        "32129",
        "19358721",
        "14362014",
        "9331508",
        "21650966",
        "37731532",
        "21564391",
        "2070535",
        "21658672",
        "19024948",
        "26379729",
        "9322277",
        "20365318",
        "26549574",
        "26519933",
        "21986488",
        "21094713",
        "16397258",
        "39544699",
        "32112",
        "9805053",
        "39849797",
        "35590956",
        "23928584",
        "26287625",
        "14360570",
        "21110655",
        "19361574",
        "22621582",
        "16293211",
        "13986250",
        "9302607",
        "9805194",
        "20021524",
        "38591533",
        "9306278",
        "22607369",
        "25719206",
        "26520688",
        "34817907",
        "33305163",
        "14371869",
        "19357516",
        "19357590",
        "34540768",
        "14360506",
        "20017340",
        "14350784",
        "2767059",
        "14253207",
        "23563450",
        "14360386",
        "24214088",
        "2349410",
        "14291780",
        "24896705",
        "19355562",
        "20717958",
        "21133352",
        "19362160",
        "20023569",
        "36406512",
        "35960913",
        "19359904",
        "20028816",
        "2766367",
        "37119553",
        "9807856",
        "26253023",
        "26120084",
        "9337356",
        "19193869",
        "14360080",
        "36964568",
        "19358784",
        "35289950",
        "9312190",
        "13566973",
        "21101701",
        "38690683",
        "19338316",
        "26051650",
        "26520464",
        "21677333",
        "26196437",
        "19356610",
        "21580639",
        "14361575",
        "9801641",
        "20042839",
        "20949114",
        "34001693",
        "37572263",
        "19361350",
        "34540113",
        "2760363",
        "21685166",
        "26296587",
        "22906155",
        "35591059",
        "20046323",
        "35894495",
        "1400564",
        "20015050",
        "35810511",
        "25959784",
        "19356515",
        "36301800",
        "21753123",
        "20026740",
        "26254732",
        "23697280",
        "34047020",
        "23926846",
        "9326464",
        "22199930",
        "20015535",
        "19390819",
        "35264721",
        "20630973",
        "26237202",
        "19362154",
        "9338500",
        "39025",
        "9336500",
        "9304612",
        "9805171",
        "9620081",
        "9303328",
        "9311380",
        "9351600",
        "9807862",
        "9323408",
        "2068095",
        "9809192",
        "9333401",
        "9305480",
        "9356307",
        "1904694",
        "9328601",
        "9806443",
        "9315357",
        "9801546",
        "9804355",
        "9334702",
        "9804119",
        "39002",
        "9807750",
        "9806354",
        "9325703",
        "9353504",
        "9807595",
        "39019",
        "2073574",
        "9806437",
        "9322299",
        "5839888",
        "32129",
        "9331508",
        "2070535",
        "9322277",
        "32112",
        "9805053",
        "9302607",
        "9805194",
        "9306278",
        "2767059",
        "2349410",
        "2766367",
        "9807856",
        "9337356",
        "9312190",
        "9801641",
        "2760363",
        "1400564",
        "9326464",
    ];

    const status_fields = [
        'addition_firstname_extendedstatus',
        'addition_lastname_extendedstatus',
        'amount_extendedstatus',
        'assetsCurrency_extendedstatus',
        'brand_extendedstatus',
        'cost_extendedstatus',
        'cost_percent_extendedstatus',
        'costAssessment_extendedstatus',
        'costDate_extendedstatus',
        'costDateOrigin_extendedstatus',
        'costDateUse_extendedstatus',
        'country_extendedstatus',
        'dateUse_extendedstatus',
        'descriptionObject_extendedstatus',
        'emitent_eng_company_name_extendedstatus',
        'emitent_eng_fullname_extendedstatus',
        'emitent_extendedstatus',
        'emitent_ua_company_name_extendedstatus',
        'emitent_ua_fullname_extendedstatus',
        'emitent_ukr_company_name_extendedstatus',
        'emitent_ukr_fullname_extendedstatus',
        'en_name_extendedstatus',
        'graduationYear_extendedstatus',
        'incomeSource_extendedstatus',
        'manufacturerName_extendedstatus',
        'model_extendedstatus',
        'name_extendedstatus',
        'objectType_extendedstatus',
        'organization_eng_company_name_extendedstatus',
        'organization_ua_company_name_extendedstatus',
        'organization_ukr_company_name_extendedstatus',
        'otherObjectType_extendedstatus',
        'owningDate_extendedstatus',
        'propertyDescr_extendedstatus',
        'sizeAssets_extendedstatus',
        'sizeIncome_extendedstatus',
        'source_eng_company_name_extendedstatus',
        'source_ua_company_name_extendedstatus',
        'source_ukr_company_name_extendedstatus',
        'totalArea_extendedstatus',
        'trademark_extendedstatus'
    ];

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
    };
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
    };
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
    };

    const exchange_rates_2018 = {
        "AMD": 0.058164,
        "AUD": 19.55852,
        "AZN": 16.28721,
        "BGN": 16.21543,
        "BRL": 7.136151,
        "BYR": 12.81864,
        "CAD": 20.32697,
        "CHF": 28.2481,
        "CLP": 0.039925,
        "CNY": 4.025761,
        "CZK": 1.230279,
        "DKK": 4.247069,
        "EGP": 1.55079,
        "EUR": 31.71414,
        "GBP": 35.13137,
        "GEL": 10.55293,
        "HKD": 3.534948,
        "HRK": 4.280199,
        "HUF": 0.098611,
        "ILS": 7.353491,
        "INR": 0.395312,
        "IQD": 0.023788,
        "IRR": 0.000659,
        "ISK": 0.237994,
        "JPY": 0.250903,
        "KGS": 0.404048,
        "KRW": 0.024789,
        "KWD": 91.38041,
        "KZT": 0.07278,
        "LBP": 0.018744,
        "LYD": 20.27643,
        "MDL": 1.615164,
        "MNT": 0.010579,
        "MXN": 1.406055,
        "NOK": 3.179745,
        "NZD": 18.58976,
        "PEN": 8.216102,
        "PKR": 0.210775,
        "PLN": 7.370581,
        "RON": 6.80123,
        "RUB": 0.39827,
        "SAR": 7.383537,
        "SEK": 3.085843,
        "SGD": 20.27499,
        "SYP": 0.053766,
        "TJS": 2.996397,
        "TMT": 8.063647,
        "TRY": 5.250685,
        "TWD": 0.917903,
        "UAH": 1,
        "USD": 27.68826,
        "UZS": 0.003401,
        "VND": 0.00121,
        "XDR": 38.5086,
        "XOF": 0.04834,
        "QAR": 7.606666,
        "AED": 7.684891,
        "UYU": 0.855104,
        "GHS": 5.855102,
        "BDT": 0.337391,
        "BYN": 12.81983,
        "DZD": 0.239079,
        "IDR": 0.001906,
        "MAD": 2.976112,
        "MYR": 6.744559,
        "RSD": 0.272578,
        "THB": 0.858366,
        "TND": 9.658384,
        "ZAR": 1.927841,
    };
    const exchange_rates_2019 = {
        "AMD": 0.049398,
        "AUD": 16.5223,
        "AZN": 13.9265,
        "BGN": 13.5087,
        "BRL": 5.8477,
        "BYR": 11.2256872,
        "CAD": 18.1011,
        "CHF": 24.2711,
        "CLP": 0.031832012,
        "CNY": 3.3858,
        "CZK": 1.0357,
        "DKK": 3.5382,
        "EGP": 1.4769,
        "EUR": 26.422,
        "GBP": 31.0206,
        "GEL": 8.2747,
        "HKD": 3.0419,
        "HRK": 3.5481,
        "HUF": 0.079881,
        "ILS": 6.843,
        "INR": 0.3319,
        "IQD": 0.019904,
        "IRR": 0.00056396,
        "ISK": 0.195495213,
        "JPY": 0.21626,
        "KGS": 0.33985,
        "KRW": 0.020399,
        "KWD": 78.17227723,
        "KZT": 0.062177,
        "LBP": 0.015712,
        "LYD": 16.8777,
        "MDL": 1.3705,
        "MNT": 0.0086762,
        "MXN": 1.2521,
        "NOK": 2.6807,
        "NZD": 15.878,
        "PEN": 7.155951662,
        "PKR": 0.152942468,
        "PLN": 6.1943,
        "RON": 5.5255,
        "RUB": 0.3816,
        "SAR": 6.3116,
        "SEK": 2.533,
        "SGD": 17.5168,
        "SYP": 0.054451034,
        "TJS": 2.443,
        "TMT": 6.7675,
        "TRY": 3.9757,
        "TWD": 0.78645,
        "UAH": 1,
        "USD": 23.6862,
        "UZS": 0.002489,
        "VND": 0.0010221,
        "XDR": 32.6996,
        "XOF": 0.040529414,
        "QAR": 6.507197802,
        "AED": 6.4489,
        "UYU": 0.62861465,
        "GHS": 4.1193,
        "BDT": 0.27899,
        "BYN": 11.2577,
        "DZD": 0.19841,
        "IDR": 0.0016976,
        "MAD": 2.4677,
        "MYR": 5.7368,
        "RSD": 0.22477,
        "THB": 0.78556,
        "TND": 8.3827,
        "ZAR": 1.687,
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
          huge_prize_threshold = 10000;

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
        family_member_did_not_provide_information = false;
        has_huge_prize = false;
        has_bo_abroad = false;
        has_non_bank_liabilities = false;

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
            let exchange_table = exchange_rates_2019;
            if (nacp_doc.step_0.declarationYear1 == '2015')
                exchange_table = exchange_rates_2015;
            if (nacp_doc.step_0.declarationYear1 == '2016')
                exchange_table = exchange_rates_2016;
            if (nacp_doc.step_0.declarationYear1 == '2017')
                exchange_table = exchange_rates_2017;
            if (nacp_doc.step_0.declarationYear1 == '2018')
                exchange_table = exchange_rates_2018;
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

            if (estate_doc.dnt_costDate_hidden && estate_doc.dnt_costAssessment_hidden && owning_date.length == 3) {
                const owning_year = parseInt(owning_date[2]);
                if (owning_year && owning_year + 5 >= parseInt(nacp_doc.step_0.declarationYear1))
                    estate_has_hidden_cost = true;
            }


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
            if (corp_doc.country != "" && typeof(corp_doc.country) != "undefined" && corp_doc.country != '1')
                corprights_has_foreign = true;
            if (String(corp_doc.person) in (nacp_doc.step_2 || {}) && corp_doc.dnt_cost_hidden)
                hidden_in_family = true;
        }
    }
    if (nacp_doc.step_9) {
        for (let key in nacp_doc.step_9) {
            const bo_doc = nacp_doc.step_9[key];
            if (typeof(bo_doc) != 'object')
                continue;

            if (bo_doc.country != "" && typeof(bo_doc.country) != "undefined" && bo_doc.country != '1')
                has_bo_abroad = true;

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

            if (income_doc.dnt_objectType_encoded == 'other') {
                const income_type = income_doc.otherObjectType.toLowerCase();

                for (let prize_marker of [/\Bвигра/i, /\Bлотере/i, /мегалот/i, /суперлото/i, /\Bпризові\B/i, /\Bпризи\B/i, /\Bпризів\B/i]) {
                    if (prize_marker.test(income_type)) {
                        total_prizes += income_doc.sizeIncome;
                        break
                    }
                }
            }
            total_income += income_doc.sizeIncome;
        }
    }
    if (nacp_doc.step_12) {
        for (let key in nacp_doc.step_12) {
            const assets_doc = nacp_doc.step_12[key];
            if (typeof(assets_doc) != 'object')
                continue;

            if ((assets_doc.dnt_objectType_encoded == 'bank' ||
                 assets_doc.dnt_objectType_encoded == 'credit_union') && assets_doc.dnt_is_foreign)
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

            let not_bank = true;
            for (let code of ["emitent_ua_company_code", "emitent_eng_company_code"]) {
                if (typeof(liability_doc[code]) === "undefined") {
                    continue;
                }
                let clean_code = liability_doc[code].replace(/^0+/, '').trim();

                if (common_bank_codes.indexOf(clean_code) != -1) {
                    not_bank = false;
                    break
                }
            }

            if (not_bank)
                for (let name of ["emitent_ua_company_name", "emitent_ukr_company_name", "emitent_eng_company_name"])
                    if (typeof(liability_doc[name]) !== "undefined") {
                        let bank_name = liability_doc[name].toLowerCase();

                        for (let name_chunk of common_bank_names)
                            if (bank_name.indexOf(name_chunk) != -1) {
                                not_bank = false;
                                break
                            }
                    }

            if (not_bank) {
                if (liability_doc.dnt_objectType_encoded != "leasing" &&
                    liability_doc.dnt_objectType_encoded != "pension" &&
                    liability_doc.dnt_objectType_encoded != "other" &&
                    liability_doc.dnt_objectType_encoded != "insurance")
                    has_non_bank_liabilities = true;

                if (liability_doc.dnt_objectType_encoded == "other") {
                    const other_object_type = liability_doc.otherObjectType.toLowerCase();
                    let skip = false;

                    for (let exclude of ["лізи", "лизи", "пенсі", "пенси", "страхув", "страхов"]) {
                        if (other_object_type.indexOf(exclude) != -1) {
                            skip = true;
                            break;
                        }
                    }

                    if (!skip)
                        has_non_bank_liabilities = true;
                }
            }

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
    has_huge_prize = total_prizes >= huge_prize_threshold;

    function find_extendedstatus3(obj) {
        for (var i in obj) {
            if (obj.hasOwnProperty(i)) {
                if (i == "step_1" || i == "step_2") {
                    continue;
                }

                if (typeof obj[i] === 'object') {
                    var foundLabel = find_extendedstatus3(obj[i]);
                    if (foundLabel) {
                        return foundLabel;
                    }
                } else if (status_fields.indexOf(String(i).toLowerCase()) !== -1 ) {
                    if (String(obj[i]) == "3") {
                        return true;
                    }
                }
            }
        }
        return false;
    };

    family_member_did_not_provide_information = find_extendedstatus3(doc);

    emit(doc._id, [doc.doc_uuid, assets_to_income, income_presents_to_total, expenses_to_inc_and_assets,
                   liabilities_to_inc_and_assets, jar_of_cash, garage_wo_car, house_no_land, has_luxury_cars,
                   has_luxury_cars_v2, vehicle_purch_no_cost, estate_purch_no_cost, estate_has_hidden_cost,
                   corprights_has_foreign, has_foreign_bank_acc, income_has_prizes, loan_shark, jar_of_pocket_cash,
                   income_presents_to_total_50, hidden_in_family,
                   total_expenses, total_liabilities, total_cash, total_presents, has_aircraft_flag, 
                   has_major_real_estate, has_foreign_real_estate, family_member_did_not_provide_information,
                   has_huge_prize, has_bo_abroad, has_non_bank_liabilities]);
}
