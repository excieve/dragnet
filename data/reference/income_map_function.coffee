(doc) ->
    if not doc.step_0? or doc.step_0.changesYear? or not doc.step_0.declarationType?
        return
    if doc.step_0.declarationType != '1'
        return

    declarant_salary_sum = 0.0
    family_salary_sum = 0.0
    declarant_total_sum = 0.0
    family_total_sum = 0.0

    if doc.step_11?
        for key, income_doc of doc.step_11
            if typeof income_doc != 'object'
                continue
            size = parseFloat(income_doc.sizeIncome.replace(',', '.')) or 0.0

            if income_doc.person == '1'
                if income_doc.objectType == 'Заробітна плата отримана за основним місцем роботи'
                    declarant_salary_sum += size
                declarant_total_sum += size
            else
                if income_doc.objectType == 'Заробітна плата отримана за основним місцем роботи'
                    family_salary_sum += size
                family_total_sum += size

    result = {
        FIO: "#{doc.step_1.lastname} #{doc.step_1.firstname} #{doc.step_1.middlename}",
        workPost: doc.step_1.workPost,
        workPlace: doc.step_1.workPlace,
        decl_year: doc.step_0.declarationYear1,
        salary_declarant_sum: declarant_salary_sum,
        salary_family_sum: family_salary_sum,
        total_income_declarant: declarant_total_sum,
        total_income_family: family_total_sum
    }

    emit doc._id, result