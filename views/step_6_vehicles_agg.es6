(doc) => {
    if (!doc.step_0 || doc.step_0.changesYear || !doc.step_0.declarationType || !doc.step_6)
        return;
    if (doc.step_0.declarationType != '1')
        return;

    let declarant_cost = 0.0,
        family_cost = 0.0,
        total_cost = 0.0,
        max_year = 0,
        all_names = '',
        has_hidden = true,
        seen_family_vehicles = new Set(),
        seen_all_vehicles = new Set();
    for (let key in doc.step_6) {
        const vehicle_doc = doc.step_6[key];
        if (typeof(vehicle_doc) != 'object')
            continue;
        if (vehicle_doc.costDate_hidden || vehicle_doc.graduationYear_hidden)
            has_hidden = true;

        const vehicle_key = `${vehicle_doc.brand}.${vehicle_doc.model}.${vehicle_doc.graduationYear}`;
        if (vehicle_doc.person == '1') {
            declarant_cost += vehicle_doc.costDate;
        } else if (String(vehicle_doc.person) in (doc.step_2 || {})) {
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
            all_names += ';';
            seen_all_vehicles.add(vehicle_key);
        }
    }
    all_names = all_names.slice(0, -1); // Remove last ";"

    emit([doc._id], [declarant_cost, family_cost, total_cost, max_year, has_hidden, all_names]);
}