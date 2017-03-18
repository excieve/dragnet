(doc) => {
    if (!doc.step_0 || doc.step_0.changesYear || !doc.step_0.declarationType)
        return;
    if (doc.step_0.declarationType != '1')
        return;

    let declarantSalarySum = 0.0,
        familySalarySum = 0.0,
        declarantTotalSum = 0.0,
        familyTotalSum = 0.0;
    if (doc.step_11) {
        for (let key in doc.step_11) {
            const incomeDoc = doc.step_11[key];
            if (typeof(incomeDoc) != 'object')
                continue;
            const isSalary = (incomeDoc.objectType == 'salarymain');

            if (incomeDoc.person == '1') {
                if (isSalary)
                    declarantSalarySum += incomeDoc.sizeIncome;
                declarantTotalSum += incomeDoc.sizeIncome;
            } else {
                if (isSalary)
                    familySalarySum += incomeDoc.sizeIncome;
                familyTotalSum += incomeDoc.sizeIncome;
            }
        };
    }

    const result = {
        FIO: `${doc.step_1.lastname} ${doc.step_1.firstname} ${doc.step_1.middlename}`,
        workPost: doc.step_1.workPost,
        workPlace: doc.step_1.workPlace,
        decl_year: doc.step_0.declarationYear1,
        salary_declarant_sum: declarantSalarySum,
        salary_family_sum: familySalarySum,
        total_income_declarant: declarantTotalSum,
        total_income_family: familyTotalSum
    };

    emit(doc._id, result);
}