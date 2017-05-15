import logging
import json
import argparse
import re
from itertools import zip_longest
from functools import partial
from multiprocessing import Pool, log_to_stderr
from time import perf_counter

from cloudant import couchdb

import mappings


logging.basicConfig()
logger = log_to_stderr()
logger.setLevel(logging.INFO)


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


def preprocess_doc(doc):
    # In-place modifications to keep copying to the minimum
    step_1 = doc.get('step_1', None)
    if step_1:
        if 'workPlace' in step_1 or 'workPost' in step_1:
            pattern_classify(step_1, 'organization_group', mappings.WORK_ORGANISATION_REGEXPS)
        else:
            step_1['organization_group'] = mappings.EMPTY_MARKER
    step_11 = doc.get('step_11', None)
    if is_empty_step(step_11):
        del doc['step_11']
    else:
        for key in iterate_ugly_dict(step_11):
            normalise_numerical(doc['_id'], step_11, key, 'sizeIncome')
            normalise_empty(step_11, key, 'objectType')
            normalise_empty(step_11, key, 'incomeSource')
            encode_categories(step_11, key, 'objectType', mappings.INCOME_OBJECT_TYPE_MAPPING,
                              new_field='objectType_encoded')
            encode_booleans(step_11, key, 'source_citizen', 'is_foreign', mappings.FOREIGN_SOURCE_TAGS)
    step_6 = doc.get('step_6', None)
    if is_empty_step(step_6):
        del doc['step_6']
    else:
        for key in iterate_ugly_dict(step_6):
            normalise_numerical(doc['_id'], step_6, key, 'costDate')
            normalise_numerical(doc['_id'], step_6, key, 'graduationYear')
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
    step_3 = doc.get('step_3', None)
    if is_empty_step(step_3):
        del doc['step_3']
    else:
        for key in iterate_ugly_dict(step_3):
            normalise_numerical(doc['_id'], step_3, key, 'costDate')
            normalise_numerical(doc['_id'], step_3, key, 'costAssessment')
            normalise_numerical(doc['_id'], step_3, key, 'totalArea')
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
    step_12 = doc.get('step_12', None)
    if is_empty_step(step_12):
        del doc['step_12']
    else:
        for key in iterate_ugly_dict(step_12):
            normalise_numerical(doc['_id'], step_12, key, 'sizeAssets')
            normalise_empty(step_12, key, 'objectType')
            encode_categories(step_12, key, 'objectType', mappings.ASSET_OBJECT_TYPE_MAPPING,
                              new_field='objectType_encoded')
            encode_booleans(step_12, key, 'organization_type', 'is_foreign', mappings.FOREIGN_SOURCE_TAGS)

    step_13 = doc.get('step_13', None)
    if is_empty_step(step_13):
        del doc['step_13']
    else:
        for key in iterate_ugly_dict(step_13):
            normalise_numerical(doc['_id'], step_13, key, 'sizeObligation')
            normalise_empty(step_13, key, 'objectType')
            encode_categories(step_13, key, 'objectType', mappings.LIABILITY_OBJECT_TYPE_MAPPING,
                              new_field='objectType_encoded')
            encode_booleans(step_13, key, 'emitent_citizen', 'is_foreign', mappings.FOREIGN_SOURCE_TAGS)

    step_14 = doc.get('step_14', None)
    if is_empty_step(step_14):
        del doc['step_14']
    else:
        for key in iterate_ugly_dict(step_14):
            normalise_numerical(doc['_id'], step_14, key, 'costAmount')
            normalise_empty(step_14, key, 'specExpenses')
            encode_categories(step_14, key, 'specExpenses', mappings.EXPENSE_SPEC_MAPPING,
                              new_field='specExpenses_encoded')
    return doc


def import_batch(docs, db_config):
    """Bulk import a batch of ElasticSearch-like documents into CouchDB"""
    t1 = perf_counter()
    docs_objects = []
    for d in docs:
        if d:
            doc_object = json.loads(d)
            # Only import those declarations we know don't have any further corrections for that year
            if not doc_object['_source'].get('corrected_declarations', []):
                source = doc_object['_source']['nacp_orig']
                source.update({
                    '_id': doc_object['_id'],
                    'mapped_region': doc_object['_source']['general']['post']['region']
                })
                docs_objects.append(preprocess_doc(source))
    imported = 0
    with couchdb(db_config['user'], db_config['password'], url=db_config['url']) as couch:
        db = couch[db_config['name']]
        # When trying to bulk insert an existing document without providing a new revision ID CouchDB will
        # throw a conflict error, we'll use this to only insert new stuff without existence checks.
        imported_docs = list(filter(lambda x: x.get('error') is None, db.bulk_docs(docs_objects)))
        imported += len(imported_docs)
    t2 = perf_counter()
    return len(docs_objects), imported, t2 - t1


def grouper(iterable, n, fillvalue=None):
    """Collect data into fixed-length chunks or blocks"""
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def import_all(docs_file, db_config, concurrency, chunks_per_process):
    total_imported_docs, rates = 0, []
    with open(docs_file, 'r', encoding='utf-8') as f:
        with Pool(concurrency) as pool:
            # Lazily consume batches of `chunks_per_process` for every process in the pool of `concurrency`
            results = pool.imap(partial(import_batch, db_config=db_config),
                                grouper(f, chunks_per_process))
            for i, result in enumerate(results):
                num_docs, imported_docs, time_spent = result
                total_imported_docs += imported_docs
                rate = float(num_docs) / float(time_spent)
                rates.append(rate)
                logger.info(
                    'Batch #{} finished importing {} new documents in {:.2f}s with the rate of {:.2f}docs/s'
                    .format(i, imported_docs, time_spent, rate)
                )
    logger.info(
        'Total imported {} new documents with the avg rate of {:.2f}docs/s across all processes'
        .format(total_imported_docs, sum(rates) / float(len(rates)) * concurrency)
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Import documents from ElasticSearch-like dump to CouchDB')
    parser.add_argument('docs_file', help='Documents file')
    parser.add_argument('-u', '--username', help='CouchDB username')
    parser.add_argument('-p', '--password', help='CouchDB password')
    parser.add_argument('-d', '--dbname', help='CouchDB database name', default='declarations')
    parser.add_argument('-e', '--endpoint', help='CouchDB endpoint', default='http://localhost:5984')
    parser.add_argument('-c', '--concurrency', help='Number of processes to spawn', type=int, default=8)
    parser.add_argument('-C', '--chunks', help='Number of chunks to run in a batch', type=int, default=1500)
    parser.add_argument('-P', '--purge', help='Purge the DB before importing', action='store_true', default=False)
    args = parser.parse_args()

    db_config = {
        'user': args.username,
        'password': args.password,
        'url': args.endpoint,
        'name': args.dbname
    }

    # Ensure our DB exists before actually importing
    with couchdb(db_config['user'], db_config['password'], url=db_config['url']) as couch:
        try:
            db = couch[args.dbname]
            if args.purge:
                db.delete()
                logger.info('Database {} purged.'.format(args.dbname))
        except KeyError:
            pass
        db = couch.create_database(args.dbname, throw_on_exists=False)
        if db.exists():
            logger.info('Database {} created or already exists'.format(args.dbname))

    import_all(args.docs_file, db_config, args.concurrency, args.chunks)
