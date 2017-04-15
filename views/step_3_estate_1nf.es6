(doc) => {
    if (!doc.step_0 || doc.step_0.changesYear || !doc.step_0.declarationType || !doc.step_3)
        return;
    if (doc.step_0.declarationType != '1')
        return;

    let result_dict = {},
        person_key = '';
    for (let key in doc.step_3) {
        const estate_doc = doc.step_3[key];
        if (typeof(estate_doc) != 'object')
            continue;
        if (!estate_doc.rights)
            continue;
        if (estate_doc.totalArea_hidden && estate_doc.costDate_hidden && estate_doc.costAssessment_hidden)
            continue;

        if (estate_doc.person == '1')
            person_key = 'd';  // D is for Declarant
        else if (String(estate_doc.person) in (doc.step_2 || {}))
            person_key = 'f';  // F is for Family
        else {
            person_key = 'u';  // U is for fUcked Up
        }

        const is_foreign = estate_doc.country != '1',
              owning_date = estate_doc.owningDate.split('.'),
              is_same_year = owning_date[2] == doc.step_0.declarationYear1;
        let per_person_key = `${person_key}.${estate_doc.objectType_encoded}.${is_same_year}.${is_foreign}`,
            all_key = `all.${estate_doc.objectType_encoded}.${is_same_year}.${is_foreign}`;

        for (let right_key in estate_doc.rights) {
            const right = estate_doc.rights[right_key];
            if (!right)
                continue;
            // We only want to account for the estate once per owner, so excluding usage rights and co-ownership by others
            if (right.rightBelongs != estate_doc.person && right.rightBelongs != 'j')
                continue;
            if (right.rightBelongs == 'j' && right.ownershipType_encoded == 'comproperty')
                continue;
            const ownership = `.${right.ownershipType_encoded}`;
            for (let result_key of [per_person_key, all_key]) {
                result_key += ownership;
                if (!(result_key in result_dict))
                    result_dict[result_key] = [0, 0, 0, 0, 0];
                result_dict[result_key][0] += 1;
                result_dict[result_key][1] += estate_doc.totalArea;
                result_dict[result_key][2] = Math.max(estate_doc.totalArea, result_dict[result_key][2]);
                result_dict[result_key][3] += estate_doc.costDate;
                result_dict[result_key][4] += estate_doc.costAssessment;
            }
        }
    }

    for (let key in result_dict)
        emit([doc._id].concat(key.split('.')), result_dict[key]);
}