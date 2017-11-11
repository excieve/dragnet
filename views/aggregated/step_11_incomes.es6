(doc) => {
    const nacp_doc = doc.nacp_orig;
    if (!nacp_doc.step_0 || nacp_doc.step_0.changesYear || !nacp_doc.step_0.declarationType || !nacp_doc.step_11)
        return;

    let declarant_income = 0.0,
        family_income = 0.0,
        total_income = 0.0,
        has_hidden = false,
        has_foreign = false;
    for (let key in nacp_doc.step_11) {
        const income_doc = nacp_doc.step_11[key];
        if (typeof(income_doc) != 'object')
            continue;
        if (income_doc.sizeIncome === undefined)
            continue;
        if (income_doc.dnt_is_foreign == true)
            has_foreign = true;
        if (income_doc.dnt_sizeIncome_hidden) {
            has_hidden = true;
            continue;
        }

        if (income_doc.person == '1')
            declarant_income += income_doc.sizeIncome;
        else if (String(income_doc.person) in (nacp_doc.step_2 || {}))
            family_income += income_doc.sizeIncome;
        total_income += income_doc.sizeIncome;
    }

    let family_ratio = 0.0;
    if (total_income != 0.0)
        family_ratio = family_income / total_income;

    emit(doc._id, [doc.doc_uuid, declarant_income, family_income, total_income, has_hidden, has_foreign, family_ratio]);
}