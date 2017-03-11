let f = (doc) => {
    const incomeMapping = {
        "заробітна плата отримана за основним місцем роботи": "salarymain",
        "заробітна плата отримана за сумісництвом": "salarysecond",
        "пенсія": "pension",
        "дохід від надання майна в оренду": "leasing",
        "дохід від зайняття підприємницькою діяльністю": "business",
        "гонорари та інші виплати згідно з цивільно-правовим правочинами": "contractfee",
        "дохід від зайняття незалежною професійною діяльністю": "indepprof",
        "проценти": "interest",
        "дивіденди": "dividends",
        "роялті": "royalty",
        "страхові виплати": "insurance",
        "подарунок у негрошовій формі": "presentnomoney",
        "подарунок у грошовій формі": "presentmoney",
        "благодійна допомога": "charity",
        "приз": "prize",
        "дохід від відчуження нерухомого майна": "saleestate",
        "дохід від відчуження рухомого майна (крім цінних паперів та корпоративних прав)": "salemovable",
        "дохід від відчуження цінних паперів та корпоративних прав": "salestock",
        "спадщина": "inheritence",
        "інше": "other"        
    };

    const personValues = ["d", "f", "u"],
          geoSourceValues = ["ukr", "abr"];

    if (!doc.step_0 || doc.step_0.changesYear || !doc.step_0.declarationType)
        return;

    if (doc.step_0.declarationType != '1')
        return;

    let declarantSalarySum = 0.0,
        familySalarySum = 0.0,
        declarantTotalSum = 0.0,
        familyTotalSum = 0.0;


    let result_dict = {},
        family = [],
        person_key = "",
        source_key = "",
        geosource_key = "";

    for (let person in personValues) {
        result_dict[`income.hidden.${personValues[person]}`] = 0.0;
        for (let geo_src in geoSourceValues)
            for (let src in incomeMapping) {
                result_dict[`income.sum.${personValues[person]}.${geoSourceValues[geo_src]}.${incomeMapping[src]}`] = 0.0;
            }
    }


    if (doc.step_3) {
        family = Object.keys(doc.step_3);
    }

    if (doc.step_11) {
        for (let key in doc.step_11) {
            const incomeDoc = doc.step_11[key];
            if (typeof(incomeDoc) != 'object')
                continue;

            if (incomeDoc.person == '1')
                person_key = "d";  // D is for Declarant
            else if (incomeDoc.person in family)
                person_key = "f";  // F is for Family
            else
                person_key = "u";  // U is for fUcked Up

            if (incomeDoc.objectType.toLowerCase() in incomeMapping)
                source_key = incomeMapping[incomeDoc.objectType.toLowerCase()]
            else
                source_key = "other";

            if (incomeDoc.source_citizen.toLowerCase() in [
                    "іноземний громадянин",
                    "юридична особа, зареєстрована за кордоном"])
                geosource_key = "abr";
            else
                geosource_key = "ukr";

            val = Number.parseInt(incomeDoc.sizeIncome);

            if (!Number.isNaN(val))
                result_dict[`income.sum.${person_key}.${geosource_key}.${source_key}`] += val;
            else
                result_dict[`income.hidden.$(person_key)`] = 1;
        };
    }

    return(doc._id, result_dict);
}

let json_data = require('../../test_assets/poroshenko_jr.json')
console.log(f(json_data["data"]))

json_data = require('../../test_assets/poroshenko.json')
console.log(f(json_data["data"]))

json_data = require('../../test_assets/derkatch.json')
console.log(f(json_data["data"]))
