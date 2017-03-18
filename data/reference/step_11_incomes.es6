(doc) => {
    if (!doc.step_0 || doc.step_0.changesYear || !doc.step_0.declarationType)
        return;

    if (doc.step_0.declarationType != '1')
        return;

    const income_mapping = {
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
        "спадщина": "inheritance",
        "інше": "other"        
    };

    const person_values = ["d", "f", "u"],
          geo_source_values = ["ukr", "abr"],
          abroad_sources = [
            "іноземний громадянин",
            "юридична особа, зареєстрована за кордоном"
          ];

    let result_dict = {},
        family = [],
        person_key = "",
        source_key = "",
        geosource_key = "";

    for (let person of person_values) {
        result_dict[`income.hidden.${person}`] = 0.0;
        for (let geo_src of geo_source_values)
            for (let src in income_mapping) {
                result_dict[`income.sum.${person}.${geo_src}.${income_mapping[src]}`] = 0.0;
            }
    }

    if (doc.step_11) {
        for (let key in doc.step_11) {
            const income_doc = doc.step_11[key];
            if (typeof(income_doc) != 'object')
                continue;

            if (income_doc.person == '1')
                person_key = "d";  // D is for Declarant
            else if (String(income_doc.person) in (doc.step_2 || {}))
                person_key = "f";  // F is for Family
            else {
                person_key = "u";  // U is for fUcked Up
            }

            source_key = income_mapping[income_doc.objectType.toLowerCase()] || "other";

            if (abroad_sources.indexOf(income_doc.source_citizen.toLowerCase()) != -1)
                geosource_key = "abr";
            else
                geosource_key = "ukr";

            if (!Number.isNaN(income_doc.sizeIncome))
                result_dict[`income.sum.${person_key}.${geosource_key}.${source_key}`] += income_doc.sizeIncome;
            else
                result_dict[`income.hidden.${person_key}`] = 1;
        };
    }

    emit(doc._id, result_dict);
}
