# -*- coding: utf-8 -*-


def fun(doc):
    if "step_0" not in doc or "changesYear" in doc["step_0"] or "declarationType" not in doc["step_0"]:
        return

    if doc["step_0"]["declarationType"] != "1":
        return

    declarant_salary_sum = 0.0
    family_salary_sum = 0.0
    declarant_total_sum = 0.0
    family_total_sum = 0.0
    if 'step_11' in doc:
        if not isinstance(doc['step_11'], dict):
            return
        for key, income_doc in doc['step_11'].items():
            if key == 'empty':
                continue

            size = income_doc['sizeIncome']
            is_salary = income_doc['objectType'] == u"Заробітна плата отримана за основним місцем роботи"

            if income_doc['person'] == '1':
                if is_salary:
                    declarant_salary_sum += size
                declarant_total_sum += size
            else:
                if is_salary:
                    family_salary_sum += size
                family_total_sum += size

    result = {
        'FIO': ' '.join([doc['step_1']['lastname'], doc['step_1']['firstname'], doc['step_1']['middlename']]),
        'workPost': doc['step_1']['workPost'],
        'workPlace': doc['step_1']['workPlace'],
        'decl_year': doc['step_0']['declarationYear1'],
        'salary_declarant_sum': declarant_salary_sum,
        'salary_family_sum': family_salary_sum,
        'total_income_declarant': declarant_total_sum,
        'total_income_family': family_total_sum
    }

    yield doc['_id'], result
