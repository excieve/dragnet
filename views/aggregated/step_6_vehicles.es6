(doc) => {
    const nacp_doc = doc.nacp_orig;
    if (!nacp_doc.step_0 || nacp_doc.step_0.changesYear || !nacp_doc.step_0.declarationType || !nacp_doc.step_6)
        return;

    let declarant_cost = 0.0,
        family_cost = 0.0,
        total_cost = 0.0,
        max_year = 0,
        all_names = '',
        has_hidden = false,
        seen_family_vehicles = new Set(),
        seen_all_vehicles = new Set();
    for (let key in nacp_doc.step_6) {
        const vehicle_doc = nacp_doc.step_6[key];
        if (typeof(vehicle_doc) != 'object')
            continue;
        if (vehicle_doc.costDate === undefined)
            continue;
        if (!vehicle_doc.brand && !vehicle_doc.model)
            has_hidden = true;

        const vehicle_key = `${vehicle_doc.brand}.${vehicle_doc.model}.${vehicle_doc.graduationYear}`;
        if (vehicle_doc.person == '1') {
            declarant_cost += vehicle_doc.costDate;
        } else if (String(vehicle_doc.person) in (nacp_doc.step_2 || {})) {
            if (!seen_family_vehicles.has(vehicle_key)) {
                family_cost += vehicle_doc.costDate;
                seen_family_vehicles.add(vehicle_key);
            }
        }

        if (!seen_all_vehicles.has(vehicle_key)) {
            total_cost += vehicle_doc.costDate;
            max_year = Math.max(max_year, vehicle_doc.graduationYear);
            if (vehicle_doc.brand)
                all_names += vehicle_doc.brand;
            if (vehicle_doc.model)
                all_names += ` ${vehicle_doc.model}`;

            if (!vehicle_doc.brand && !vehicle_doc.model)
                all_names += 'немає_даних'

            all_names += '; ';
            seen_all_vehicles.add(vehicle_key);
        }
    }
    all_names = all_names.slice(0, -2); // Remove last "; "

    emit(doc._id, [doc.doc_uuid, declarant_cost, family_cost, total_cost, max_year || '!немає даних', has_hidden, all_names,
                   seen_all_vehicles.size > 0]);
}