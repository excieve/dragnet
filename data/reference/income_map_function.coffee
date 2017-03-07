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
            is_salary = income_doc.objectType == 'Заробітна плата отримана за основним місцем роботи'

            if income_doc.person == '1'
                if is_salary
                    declarant_salary_sum += income_doc.sizeIncome
                declarant_total_sum += income_doc.sizeIncome
            else
                if is_salary
                    family_salary_sum += income_doc.sizeIncome
                family_total_sum += income_doc.sizeIncome

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