"""
Auxiliary script to compare old declarations with new declarations after the conversion.
Collects found discrepancies.
Can compare folders and collect cumullative errors
Use with care
"""

import os.path
import re
import json
import logging
from pprint import pprint
from collections import defaultdict, Counter
from copy import deepcopy
from glob import glob
from tqdm import tqdm
from .new_format_converter import DeclarationConverter, strip_empty_elements
from .nacp_parser import replace_apostrophes


logging.basicConfig()
logger = logging.getLogger("declarations_comparator")


def json_dump(d):
    return json.dumps(d, ensure_ascii=False, indent=4, sort_keys=True)


class ComparisonException(Exception):
    pass


class DeclarationComparator:
    step_options = {
        "step_2": {
            "ignore_keys": [
                "cityPath",
                "region",
                "district",
                "city",
                "country",
            ]
        },
        # TODO: Validate
        "step_3": {
            "compare_nested": ["rights"],
            "ignore_keys": ["cityPath", "district", "region"],
        },
        "step_4": {
            "compare_nested": ["rights"],
            "ignore_keys": [
                "cityPath",
                "region",
                "district",
            ]
        },
        "step_5": {"compare_nested": ["rights"]},
        "step_6": {"compare_nested": ["rights"]},
        "step_7": {"compare_nested": ["rights"]},
        "step_8": {"compare_nested": ["rights"]},
        "step_10": {"compare_nested": ["rights"]},
        "step_11": {"compare_nested": ["rights"]},
        "step_12": {"compare_nested": ["rights"]},

        # To investigate
        # "step_11": {"compare_nested": ["person"]},
        # "step_13": {"compare_nested": ["guarantor", "guarantor_realty"]},
        # "step_17": {"compare_nested": ["person"]},
    }

    def __init__(self, old_document, new_document):
        self.logging_enabled = True
        self.diff_log = defaultdict(lambda: defaultdict(set))
        self._converter = DeclarationConverter(new_document)

        with open(old_document) as fp:
            self._old = json.load(fp)

        with open(new_document) as fp:
            self._new_orig = json.load(fp)
            self._new = self._converter.convert()

        if self._old["id"] != self._new["id"]:
            raise ComparisonException(f"Cannot compare two different documents {self._old['id']} and {self._new['id']}")

    def log_difference(self, section, key, problem):
        if self.logging_enabled:
            self.diff_log[section][key].add(problem)

    def enable_logging(self):
        self.logging_enabled = True

    def disable_logging(self):
        self.logging_enabled = False

    def normalize_str(self, s):
        return replace_apostrophes(re.sub(r"\s+", " ", s).lower().strip())

    def compare_values(self, key, old_part, new_part):
        old = old_part.get(key)
        new = new_part.get(key)

        # Exit quickly
        if old == new:
            return False

        # For the cases, when new values removed or replaced because of 
        # extendedstatus flag
        # невідомо, не застосовується та член сім’ї не надав інформацію
        if str(old_part.get(f"{key}_extendedstatus", 0)) in ("1", "2", "3"):
            old = ""

        if str(new_part.get(f"{key}_extendedstatus", 0)) in ("1", "2", "3"):
            new = ""

        # For the cases when person_id is int in new documents
        if key in ["person_id"]:
            old = str(old)
            new = str(new)

        if isinstance(old, str) and isinstance(new, str):
            # For the cases of apostrophes in the names and 
            # extra spaces (god oh why)
            return self.normalize_str(old) != self.normalize_str(new)
        else:
            return old != new

    def _direct_comparison(
        self,
        old_part,
        new_part,
        section,
        key_prefix="",
        ignore_keys=None,
        compare_nested=None,
    ):
        if isinstance(old_part, (str, bool)) and isinstance(new_part, (str, bool)):
            self.log_difference(
                section,
                f"{key_prefix}",
                f"Rare case of API brainfart: cannot compare {old_part} and {new_part}",
            )
            return False

        # Let's start optimistic
        the_same = True
        if ignore_keys is None:
            ignore_keys = []

        if compare_nested is None:
            compare_nested = []

        if key_prefix:
            key_prefix += "."

        for old_k, old_v in old_part.items():
            if old_k in ignore_keys:
                continue

            if old_k in compare_nested:
                if old_k not in new_part:
                    the_same = False
                    self.log_difference(
                        section,
                        f"{key_prefix}{old_k}",
                        f"Cannot find {old_k} in the new document",
                    )

                # Rare case when old declarations has messed up rights
                if old_k == "rights" and isinstance(old_v, list):
                    old_v = self._converter.convert_rights_block(deepcopy(old_v))

                the_same = the_same and self.compare_involved_steps(
                    deepcopy(old_v),
                    deepcopy(new_part[old_k]),
                    section,
                    f"{key_prefix}{old_k}",
                )
            elif self.compare_values(old_k, old_part, new_part):
                the_same = False
                self.log_difference(
                    section,
                    f"{key_prefix}{old_k}",
                    f"Value of {old_k} in old document is {json_dump(old_v)} and it differs from {json_dump(new_part.get(old_k))} in the new document",
                )

        return the_same

    def compare_top_level(self):
        self._direct_comparison(self._old, self._new, section="_", ignore_keys=["data"])

    def compare_step0(self):
        self._direct_comparison(
            self._old["data"]["step_0"],
            self._new["data"]["step_0"],
            section="step_0",
            key_prefix="data.step_0",
        )

    def compare_step1(self):
        self._direct_comparison(
            strip_empty_elements(self._old["data"]["step_1"]),
            strip_empty_elements(self._new["data"]["step_1"]),
            section="step_1",
            key_prefix="data.step_1",
            ignore_keys=[
                "cityPath",
                "region",
                "district",
                "actual_cityPath",
                "actual_region",
                "actual_district",
                "actual_city",
                "city",
            ],
        )

    # TODO: universal comparator for the list of values
    def compare_involved_steps(
        self,
        old_part,
        new_part,
        section,
        key_prefix="",
        ignore_keys=None,
        compare_nested=None,
    ):
        the_same = True
        if ignore_keys is None:
            ignore_keys = []

        if compare_nested is None:
            compare_nested = []

        if not old_part and not new_part:
            return

        if not new_part:
            new_part = {"empty": "У суб'єкта декларування відсутні об'єкти для декларування в цьому розділі."}

        if not isinstance(old_part, dict):
            self.log_difference(
                section,
                f"{key_prefix}",
                f"{section} value is not a dict in the original document",
            )
            the_same = False

        if not isinstance(new_part, dict):
            self.log_difference(
                section,
                f"{key_prefix}",
                f"{section} value is not a dict in the converted document",
            )
            the_same = False

        if len(old_part) != len(new_part):
            self.log_difference(
                section,
                f"{key_prefix}",
                f"Number of entries in the old document is {len(old_part)}, while in the new document it's {len(new_part)}",
            )
            the_same = False

        if not old_part:
            old_part = {
                "empty": "У суб'єкта декларування відсутні об'єкти для декларування в цьому розділі."
            }

        parts_to_resolve = []
        for new_k in new_part.keys():
            if new_k in old_part:
                if type(old_part[new_k]) == type(new_part[new_k]):
                    if isinstance(new_part[new_k], dict):
                        the_same = the_same and self._direct_comparison(
                            strip_empty_elements(old_part[new_k]),
                            strip_empty_elements(new_part[new_k]),
                            section=section,
                            key_prefix=f"{key_prefix}.*",
                            ignore_keys=ignore_keys,
                            compare_nested=compare_nested,
                        )
                    elif old_part[new_k] != new_part[new_k]:
                        the_same = False
                        self.log_difference(
                            section,
                            f"{key_prefix}.{new_k}",
                            f"Value {old_part[new_k]} is different to {new_part[new_k]}",
                        )
                else:
                    the_same = False
                    self.log_difference(
                        section,
                        f"{key_prefix}.{new_k}",
                        f"Data type {type(old_part[new_k])} is different to {type(new_part[new_k])}",
                    )
                del old_part[new_k]
            else:
                parts_to_resolve.append(new_part[new_k])

        self.disable_logging()
        # Once we've compared all the dict elements with same ids, lets
        # reconcile the rest one by one but with logging disable
        for new_part in parts_to_resolve:
            for old_k, old_part_candidate in old_part.items():
                if self._direct_comparison(
                    strip_empty_elements(old_part_candidate),
                    strip_empty_elements(new_part),
                    section=section,
                    key_prefix=f"{key_prefix}.*",
                    ignore_keys=ignore_keys,
                    compare_nested=compare_nested,
                ):
                    del old_part[old_k]
                    break
        self.enable_logging()

        if len(old_part) > 0:
            the_same = False
            keys = list(old_part.keys())[:5]
            self.log_difference(
                section,
                f"{key_prefix}.*",
                f"There are {len(old_part)} items that cannot be reconcilled, for example {keys}",
            )

        return the_same

    def print_log(self):
        pprint(self.diff_log)

    def compare_everything(self, limit_to_steps=None):
        self.compare_top_level()

        if limit_to_steps is None:
            limit_to_steps = list(range(0, 18))

        for step in range(0, 18):
            if step not in limit_to_steps:
                continue
            if step == 0:
                self.compare_step0()
            elif step == 1:
                self.compare_step1()
            else:
                self.compare_involved_steps(
                    deepcopy(self._old["data"].get(f"step_{step}", {})),
                    deepcopy(self._new["data"].get(f"step_{step}", {})),
                    section=f"step_{step}",
                    key_prefix=f"data.step_{step}",
                    **(self.step_options.get(f"step_{step}", {})),
                )


class FolderComparator:
    def prepare_tasks(self, files):
        return {os.path.basename(f): f for f in files}

    def __init__(self, old_mask, new_mask, only_first=None):
        self.generalized_errors = defaultdict(set)

        self.old_files = self.prepare_tasks(glob(old_mask))
        self.new_files = self.prepare_tasks(glob(new_mask))

        if only_first is None:
            only_first = len(self.old_files)
        self.only_first = only_first
        for old_k, old_file in tqdm(list(self.old_files.items())[:only_first], desc="Processing files"):
            if old_k not in self.new_files:
                logger.warning(f"Cannot find {old_k} in new files")
                continue

            try:
                comparator = DeclarationComparator(old_file, self.new_files[old_k])

                comparator.compare_everything()
            except Exception as e:
                logger.error(f"During comparison of {old_k} the following error has occured: {e}")
                continue

            for section, details in comparator.diff_log.items():
                for path, errors in details.items():
                    for error in errors:
                        self.generalized_errors[(section, path, error)].add(old_k)

    def print_overall_stats(self, limit=None):
        print("Stats breakdown by the error")
        cnt = Counter({k: len(v) for k, v in self.generalized_errors.items()})

        for (section, path, error), occurences in cnt.most_common(limit):
            print(f"{section}/{path}/{error}: {occurences}")

    def print_stats_by_section(self):
        print("Stats breakdown by the section")
        cnt = Counter()

        for (section, _, _), ids in self.generalized_errors.items():
            cnt.update({section: len(ids)})

        total = 0
        for section, occurences in cnt.most_common():
            print(f"{section}: {occurences}")
            total += occurences

        print(f"\n\nGrand total: {total} errors per {self.only_first}")

    def print_examples(self, full_error, limit_to=10):
        assert isinstance(full_error, (str, tuple, list))

        if isinstance(full_error, str):
            if ":" in full_error:
                ids, _ = full_error.split(":", 1)
            else:
                ids = full_error

            section, path, error = ids.split("/")
        else:
            section, path, error = full_error

        for fname in list(self.generalized_errors[(section, path, error)])[:limit_to]:
            print(fname)


if __name__ == "__main__":
    comparator = DeclarationComparator(
        # Dubnevych 1
        #     "converter_data/old/9dce4690-bd23-4e43-902f-e6594c06eda7.json",
        #     "converter_data/dump/9dce4690-bd23-4e43-902f-e6594c06eda7.json",
        # Dubnevych 2
        #     "converter_data/old/2be988d5-e2ac-4009-a291-1edfef9de11c.json",
        #     "converter_data/dump/2be988d5-e2ac-4009-a291-1edfef9de11c.json",
        # Zelenskyi
        #     "converter_data/old/dbfd6951-3d06-4720-bc4a-fd9cf94042d0.json",
        #     "converter_data/api/dbfd6951-3d06-4720-bc4a-fd9cf94042d0.json",
        #     Poroshenko
        "converter_data/old/539d7fe3-7cfa-4d88-8a97-070b0841f56e.json",
        "converter_data/api/539d7fe3-7cfa-4d88-8a97-070b0841f56e.json",
    )

    comparator.compare_everything()
    comparator.print_log()
