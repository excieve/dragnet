[._id,
    {
        FIO: [.step_1.lastname, .step_1.firstname, .step_1.middlename] | join(" "),
        workPost: .step_1.workPost,
        workPlace: .step_1.workPlace,
        decl_year: .step_0.declarationYear1,
        total_income_declarant: [.step_11[] | select(.person == "1") | .sizeIncome | tonumber] | add,
        total_income_family: [.step_11[] | select(.person != "1") | .sizeIncome | tonumber] | add,
        salary_declarant_sum: [.step_11[] | select(.person == "1" and .objectType == "Заробітна плата отримана за основним місцем роботи") | .sizeIncome | tonumber] | add,
        salary_family_sum: [.step_11[] | select(.person != "1" and .objectType == "Заробітна плата отримана за основним місцем роботи") | .sizeIncome | tonumber] | add
    }
]