(doc) => {
    if (!doc.step_0 || doc.step_0.changesYear || !doc.step_0.declarationType || !doc.step_6)
        return;
    if (doc.step_0.declarationType != '1')
        return;

    let result_dict = {},
        person_key = '';
    for (let key in doc.step_6) {
        const vehicle_doc = doc.step_6[key];
        if (typeof(vehicle_doc) != 'object')
            continue;
        if (!vehicle_doc.rights)
            continue;
        if (vehicle_doc.costDate_hidden && vehicle_doc.graduationYear_hidden)
            continue;

        if (vehicle_doc.person == '1')
            person_key = 'd';  // D is for Declarant
        else if (String(vehicle_doc.person) in (doc.step_2 || {}))
            person_key = 'f';  // F is for Family
        else {
            person_key = 'u';  // U is for fUcked Up
        }

        const owning_date = vehicle_doc.owningDate.split('.'),
              is_same_year = owning_date[2] == doc.step_0.declarationYear1;
        let per_person_key = `${person_key}.${vehicle_doc.objectType_encoded}.${is_same_year}`,
            all_key = `all.${vehicle_doc.objectType_encoded}.${is_same_year}`;

        for (let right_key in vehicle_doc.rights) {
            const right = vehicle_doc.rights[right_key];
            if (!right || typeof(right) != 'object')
                continue;
            // We only want to account for the vehicle once per owner, so excluding usage rights and co-ownership by others
            if (right.rightBelongs != vehicle_doc.person && right.rightBelongs != 'j')
                continue;
            if (right.rightBelongs == 'j' && right.ownershipType_encoded == 'comproperty')
                continue;
            const ownership = `.${right.ownershipType_encoded}`;
            for (let result_key of [per_person_key, all_key]) {
                result_key += ownership;
                if (!(result_key in result_dict))
                    result_dict[result_key] = [0, 0, 0, 0, ''];
                result_dict[result_key][0] += 1;
                result_dict[result_key][1] += vehicle_doc.costDate;
                result_dict[result_key][2] = Math.max(vehicle_doc.costDate, result_dict[result_key][2]);
                result_dict[result_key][3] = Math.max(vehicle_doc.graduationYear, result_dict[result_key][3]);
                if (vehicle_doc.brand)
                    result_dict[result_key][4] += vehicle_doc.brand;
                if (vehicle_doc.model)
                    result_dict[result_key][4] += ` ${vehicle_doc.model}`;
                result_dict[result_key][4] += ';';
            }
        }
    }

    for (let key in result_dict)
        emit([doc._id].concat(key.split('.')), result_dict[key]);
}