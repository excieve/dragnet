import re
import logging

import mappings


logger = logging.getLogger('dragnet.nacp_normaliser')


def iterate_ugly_dict(parent):
    if not isinstance(parent, dict):
        return []
    for key in parent:
        if key == 'empty' or not isinstance(parent[key], dict):
            continue
        yield key


def normalise_numerical(doc_id, parent, key, field):
    # Normalize numerical values to floats
    try:
        parent[key][field] = float(str(parent[key][field]).strip().replace(',', '.'))
        parent[key]['{}_hidden'.format(field)] = False
    except Exception:
        value = parent[key].get(field)
        if value:
            logger.info('Wrong "{}" field value for doc ID {}: {}'
                        .format(field, doc_id, value))
        parent[key][field] = 0
        parent[key]['{}_hidden'.format(field)] = True


def normalise_empty(parent, key, field):
    value = str(parent[key].get(field, '')).strip()
    if not value or 'конфіденц' in value.lower() or 'не надав' in value.lower():
        parent[key][field] = mappings.EMPTY_MARKER
    else:
        parent[key][field] = value


def encode_categories(parent, key, field, mapping, new_field=None):
    category = parent[key].get(field, None)
    if category is not None:
        value = mapping.get(str(category).lower().strip(), 'other')
        if new_field:
            parent[key][new_field] = value
        else:
            parent[key][field] = value


def encode_booleans(parent, key, field, new_field, tags, delete_original=True):
    tag_value = parent[key].get(field, None)
    parent[key][new_field] = mappings.EMPTY_MARKER
    if tag_value is not None:
        parent[key][new_field] = str(tag_value).lower().strip() in tags
        if delete_original:
            del parent[key][field]


def is_empty_step(step):
    # Because reasons
    return (isinstance(step, list) and (len(step) == 0 or len(step[0]) == 0)) or\
           (isinstance(step, dict) and 'empty' in step)


def transform_bad_list(data, key_field):
    # Some parts of the dataset are odd-looking lists instead of dicts as in majority of cases
    result = {}
    for item in data:
        if item and isinstance(item, dict):
            key = item.get(key_field, None)
            if key is not None:
                result[key] = item
    return result


def pattern_classify(parent, new_field, mapping):
    parent[new_field] = 'Без категорії'
    for field, pattern, group in mapping:
        field_value = parent.get(field, None)
        if field_value is not None and re.search(pattern, field_value.strip().lower()) is not None:
            parent[new_field] = group
            break


def preprocess_nacp_doc(source):
    # In-place modifications to keep copying to the minimum
    doc = source['nacp_orig']
    step_1 = doc.get('step_1', None)
    if step_1:
        if 'workPlace' in step_1 or 'workPost' in step_1:
            pattern_classify(step_1, 'organization_group', mappings.WORK_ORGANISATION_REGEXPS)
        else:
            step_1['organization_group'] = mappings.EMPTY_MARKER
    step_2 = doc.get('step_2', None)
    if is_empty_step(step_2):
        del doc['step_2']
    step_3 = doc.get('step_3', None)
    if is_empty_step(step_3):
        del doc['step_3']
    else:
        for key in iterate_ugly_dict(step_3):
            normalise_numerical(source['_id'], step_3, key, 'costDate')
            normalise_numerical(source['_id'], step_3, key, 'costAssessment')
            normalise_numerical(source['_id'], step_3, key, 'totalArea')
            normalise_empty(step_3, key, 'objectType')
            encode_categories(step_3, key, 'objectType', mappings.ESTATE_OBJECT_TYPE_MAPPING,
                              new_field='objectType_encoded')
            rights = step_3[key].get('rights', None)
            if isinstance(rights, list):
                rights = transform_bad_list(rights, 'rightBelongs')
                step_3[key]['rights'] = rights
            for right_key in iterate_ugly_dict(rights):
                normalise_empty(rights, right_key, 'ownershipType')
                encode_categories(rights, right_key, 'ownershipType', mappings.PROPERTY_TYPE_MAPPING,
                                  new_field='ownershipType_encoded')
    step_4 = doc.get('step_4', None)
    if is_empty_step(step_4):
        del doc['step_4']
    else:
        for key in iterate_ugly_dict(step_4):
            normalise_numerical(source['_id'], step_4, key, 'totalArea')
            normalise_empty(step_4, key, 'objectType')
            encode_categories(step_4, key, 'objectType', mappings.ESTATE_OBJECT_TYPE_MAPPING,
                              new_field='objectType_encoded')
            rights = step_4[key].get('rights', None)
            if isinstance(rights, list):
                rights = transform_bad_list(rights, 'rightBelongs')
                step_4[key]['rights'] = rights
            for right_key in iterate_ugly_dict(rights):
                normalise_empty(rights, right_key, 'ownershipType')
                encode_categories(rights, right_key, 'ownershipType', mappings.PROPERTY_TYPE_MAPPING,
                                  new_field='ownershipType_encoded')
    step_5 = doc.get('step_5', None)
    if is_empty_step(step_5):
        del doc['step_5']
    else:
        for key in iterate_ugly_dict(step_5):
            normalise_numerical(source['_id'], step_5, key, 'costDateUse')
            normalise_empty(step_5, key, 'objectType')
            rights = step_5[key].get('rights', None)
            if isinstance(rights, list):
                rights = transform_bad_list(rights, 'rightBelongs')
                step_5[key]['rights'] = rights
            for right_key in iterate_ugly_dict(rights):
                normalise_empty(rights, right_key, 'ownershipType')
    step_6 = doc.get('step_6', None)
    if is_empty_step(step_6):
        del doc['step_6']
    else:
        for key in iterate_ugly_dict(step_6):
            normalise_numerical(source['_id'], step_6, key, 'costDate')
            normalise_numerical(source['_id'], step_6, key, 'graduationYear')
            normalise_empty(step_6, key, 'objectType')
            encode_categories(step_6, key, 'objectType', mappings.VEHICLE_OBJECT_TYPE_MAPPING,
                              new_field='objectType_encoded')
            rights = step_6[key].get('rights', None)
            if isinstance(rights, list):
                rights = transform_bad_list(rights, 'rightBelongs')
                step_6[key]['rights'] = rights
            for right_key in iterate_ugly_dict(rights):
                normalise_empty(rights, right_key, 'ownershipType')
                encode_categories(rights, right_key, 'ownershipType', mappings.PROPERTY_TYPE_MAPPING,
                                  new_field='ownershipType_encoded')
    step_7 = doc.get('step_7', None)
    if is_empty_step(step_7):
        del doc['step_7']
    else:
        for key in iterate_ugly_dict(step_7):
            normalise_numerical(source['_id'], step_7, key, 'amount')
            normalise_numerical(source['_id'], step_7, key, 'cost')
            normalise_empty(step_7, key, 'emitent_type')
            normalise_empty(step_7, key, 'typeProperty')
            rights = step_7[key].get('rights', None)
            if isinstance(rights, list):
                rights = transform_bad_list(rights, 'rightBelongs')
                step_7[key]['rights'] = rights
            for right_key in iterate_ugly_dict(rights):
                normalise_empty(rights, right_key, 'ownershipType')
    step_8 = doc.get('step_8', None)
    if is_empty_step(step_8):
        del doc['step_8']
    else:
        for key in iterate_ugly_dict(step_8):
            normalise_numerical(source['_id'], step_8, key, 'cost')
            normalise_numerical(source['_id'], step_8, key, 'cost_percent')
            normalise_empty(step_8, key, 'legalForm')
            rights = step_8[key].get('rights', None)
            if isinstance(rights, list):
                rights = transform_bad_list(rights, 'rightBelongs')
                step_8[key]['rights'] = rights
            for right_key in iterate_ugly_dict(rights):
                normalise_empty(rights, right_key, 'ownershipType')
    step_9 = doc.get('step_9', None)
    if is_empty_step(step_9):
        del doc['step_9']
    else:
        for key in iterate_ugly_dict(step_9):
            normalise_empty(step_9, key, 'legalForm')
    step_10 = doc.get('step_10', None)
    if is_empty_step(step_10):
        del doc['step_10']
    step_11 = doc.get('step_11', None)
    if is_empty_step(step_11):
        del doc['step_11']
    else:
        for key in iterate_ugly_dict(step_11):
            normalise_numerical(source['_id'], step_11, key, 'sizeIncome')
            normalise_empty(step_11, key, 'objectType')
            normalise_empty(step_11, key, 'incomeSource')
            encode_categories(step_11, key, 'objectType', mappings.INCOME_OBJECT_TYPE_MAPPING,
                              new_field='objectType_encoded')
            encode_booleans(step_11, key, 'source_citizen', 'is_foreign', mappings.FOREIGN_SOURCE_TAGS)
    step_12 = doc.get('step_12', None)
    if is_empty_step(step_12):
        del doc['step_12']
    else:
        for key in iterate_ugly_dict(step_12):
            normalise_numerical(source['_id'], step_12, key, 'sizeAssets')
            normalise_empty(step_12, key, 'objectType')
            encode_categories(step_12, key, 'objectType', mappings.ASSET_OBJECT_TYPE_MAPPING,
                              new_field='objectType_encoded')
            encode_booleans(step_12, key, 'organization_type', 'is_foreign', mappings.FOREIGN_SOURCE_TAGS)

    step_13 = doc.get('step_13', None)
    if is_empty_step(step_13):
        del doc['step_13']
    else:
        for key in iterate_ugly_dict(step_13):
            normalise_numerical(source['_id'], step_13, key, 'sizeObligation')
            normalise_empty(step_13, key, 'objectType')
            encode_categories(step_13, key, 'objectType', mappings.LIABILITY_OBJECT_TYPE_MAPPING,
                              new_field='objectType_encoded')
            encode_booleans(step_13, key, 'emitent_citizen', 'is_foreign', mappings.FOREIGN_SOURCE_TAGS)

    step_14 = doc.get('step_14', None)
    if is_empty_step(step_14):
        del doc['step_14']
    else:
        for key in iterate_ugly_dict(step_14):
            normalise_numerical(source['_id'], step_14, key, 'costAmount')
            normalise_empty(step_14, key, 'specExpenses')
            encode_categories(step_14, key, 'specExpenses', mappings.EXPENSE_SPEC_MAPPING,
                              new_field='specExpenses_encoded')
    step_15 = doc.get('step_15', None)
    if is_empty_step(step_15):
        del doc['step_15']
    step_16 = doc.get('step_16', None)
    if is_empty_step(step_16):
        del doc['step_16']

    return source
