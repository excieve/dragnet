(doc) => {
    if (!doc.step_0 || doc.step_0.changesYear || !doc.step_0.declarationType || !doc.step_11)
        return;
    if (doc.step_0.declarationType != '1')
        return;

    let result_dict = {},
        person_key = '';
    for (let key in doc.step_11) {
        const income_doc = doc.step_11[key];
        if (typeof(income_doc) != 'object')
            continue;
        if (income_doc.sizeIncome_hidden)
            continue;

        if (income_doc.person == '1')
            person_key = 'd';  // D is for Declarant
        else if (String(income_doc.person) in (doc.step_2 || {}))
            person_key = 'f';  // F is for Family
        else {
            person_key = 'u';  // U is for fUcked Up
        }

        const result_key = `${person_key}.${income_doc.objectType_encoded}.${income_doc.is_foreign}`;
        if (result_key in result_dict)
            result_dict[result_key] += income_doc.sizeIncome;
        else
            result_dict[result_key] = income_doc.sizeIncome;
    }

    for (let key in result_dict)
        emit([doc._id].concat(key.split('.')), result_dict[key]);
}