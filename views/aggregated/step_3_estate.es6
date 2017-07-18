(doc) => {
    const nacp_doc = doc.nacp_orig;
    if (!nacp_doc.step_0 || nacp_doc.step_0.changesYear || !nacp_doc.step_0.declarationType || !nacp_doc.step_3)
        return;
    if (nacp_doc.step_0.declarationType != '1')
        return;

    let declarant_land = 0.0,
        family_land = 0.0,
        total_land = 0.0,
        declarant_other = 0.0,
        family_other = 0.0,
        total_other = 0.0,
        has_hidden = false,
        has_foreign = false,
        seen_family_estates = new Set(),
        seen_all_estates = new Set();
    for (let key in nacp_doc.step_3) {
        const estate_doc = nacp_doc.step_3[key];
        if (typeof(estate_doc) != 'object')
            continue;
        if (estate_doc.totalArea === undefined)
            continue;
        if (estate_doc.country != '1')
            has_foreign = true;
        if (estate_doc.totalArea_hidden) {
            has_hidden = true;
            continue;
        }

        const estate_key = `${estate_doc.ua_cityType}.${estate_doc.totalArea}.${estate_doc.objectType_encoded}`;
        if (estate_doc.person == '1') {
            if (estate_doc.objectType_encoded == 'land')
                declarant_land += estate_doc.totalArea;
            else
                declarant_other += estate_doc.totalArea;
        } else if (String(estate_doc.person) in (nacp_doc.step_2 || {})) {
            if (!seen_family_estates.has(estate_key)) {
                if (estate_doc.objectType_encoded == 'land')
                    family_land += estate_doc.totalArea;
                else
                    family_other += estate_doc.totalArea;
                seen_family_estates.add(estate_key);
            }
        }

        if (!seen_all_estates.has(estate_key)) {
            if (estate_doc.objectType_encoded == 'land')
                total_land += estate_doc.totalArea;
            else
                total_other += estate_doc.totalArea;
            seen_all_estates.add(estate_key);
        }
    }

    emit(doc._id, [doc.doc_uuid, declarant_land, declarant_other, family_land, family_other, total_land, total_other, has_hidden,
                   has_foreign]);
}
