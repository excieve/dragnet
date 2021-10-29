"""
Script to convert declarations in the new format (both, returned by API and found in new dumps)
to the format, compatible with a previous one
"""
import json
from datetime import datetime
from dateutil.parser import parse as dt_parse
from collections import OrderedDict


class LastUpdatedOrderedDict(OrderedDict):
    "Store items in the order the keys were last added"

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.move_to_end(key)


class ParsingException(Exception):
    pass


class DeclarationConverter:
    iteration = 0
    _current_iteration = "ignore_me"
    _steps_to_unroll = [
        "step_2",
        "step_3",
        "step_4",
        "step_5",
        "step_6",
        "step_7",
        "step_8",
        "step_9",
        "step_10",
        "step_11",
        "step_12",
        "step_13",
        "step_14",
        "step_15",
        "step_16",
        "step_17",
    ]

    def __init__(self, document):
        with open(document) as fp:
            self._data = json.load(fp)
            self._document = document
            self._id = self._data["id"]
            if "schema_version" in self._data:
                self.schema_version = int(self._data["schema_version"])
            else:
                self.schema_version = 1

    def get_next_iteration(self, current_iteration):
        if current_iteration is not None:
            return str(current_iteration)

        self.iteration += 1

        return f"{self._current_iteration}_{self.iteration}"

    def raise_parsing_exception(self, error):
        raise ParsingException(
            f"Declaration #{self._id} ({self._document}) has a parsing error {error}"
        )

    def convert_rights_block(self, rights):
        rights_dict = {}

        for r in rights:
            # невідомо, не застосовується та член сім’ї не надав інформацію
            if r.get("percent-ownership_extendedstatus") in ["1", "2"] and r.get(
                "percent-ownership"
            ) in [None, "[Не застосовується]", "", "[Не відомо]"]:
                r["percent-ownership"] = "100"

            if "rightBelongs" in r and str(r["rightBelongs"]).isdigit():
                rights_dict[str(r["rightBelongs"])] = self.apply_boolean_fix(r)
            else:
                rights_dict[self.get_next_iteration(None)] = self.apply_boolean_fix(r)

        return rights_dict

    def apply_boolean_fix(self, section):
        for bool_key in [
            "sameRegLivingAddress",
            "acqBeforeFD",
            "changedName",
            "source_ua_sameRegLivingAddress",
            "debtor_ua_sameRegLivingAddress",
            "ua_sameRegLivingAddress",
            "belongsSubjectOfDeclaration",
            "builtMaterialsOrFunds",
            "dontRegistered",
            "exploitation",
            "no_taxNumber",
            "isThirdOwner",
            "unfinishConstruct",
            "guarantor_exist_",
            "guarantor_realty_exist_",
            "builtOnTerritoryOrRent",
            "emitent_ua_sameRegLivingAddress",
            "person_open_account_ua_same_reg_actual_address",
            "person_has_account_ua_same_reg_actual_address",
            "actualAddressEqualRegAddress",
        ]:
            if isinstance(section, dict) and bool_key in section:
                section[bool_key] = str(section[bool_key]) == "1"

        return section

    def rename_person_dict(self, section):
        if "person_who_care" in section:
            res = {}

            for person_block in section["person_who_care"]:
                res[person_block["person"]] = person_block

            section["person"] = res

        return section

    def remove_data_key(self):
        dt = self._data["data"]
        
        # TODO: Preprocess steps 2-8 too?
        for step in range(9, 18):
            if not dt.get(f"step_{step}"):
                dt[f"step_{step}"] = {"isNotApplicable": 1}
        for k, v in dt.items():
            if isinstance(v, dict):
                subk = list(v.keys())
                if ["isNotApplicable"] == subk:
                    dt[k] = {
                        "empty": "У суб'єкта декларування відсутні об'єкти для декларування в цьому розділі."
                    }
                    continue

                if ["data"] == subk:
                    v = v["data"]

                    if k in self._steps_to_unroll:
                        if k == "step_16":
                            for org in v:
                                orgval = dict()

                                for orgval_entry in v[org]:
                                    orgval[
                                        self.get_next_iteration(
                                            orgval_entry.get("iteration")
                                        )
                                    ] = orgval_entry

                                v[org] = orgval

                            for required_org_k in ["org", "part_org"]:
                                if required_org_k not in v:
                                    v[required_org_k] = []

                            dt[k] = v
                        elif not isinstance(v, list):
                            self.raise_parsing_exception(
                                f"Expecting an array for the {k}"
                            )
                        else:
                            subval = LastUpdatedOrderedDict()

                            for i, step_data in enumerate(v):
                                step_data = self.apply_boolean_fix(step_data)
                                step_data = self.rename_person_dict(step_data)

                                if "rights" in step_data:
                                    step_data["rights"] = self.convert_rights_block(
                                        step_data["rights"]
                                    )

                                # Check for the form of changes

                                if k == "step_2" and self._data.get("type") != 2:
                                    subval[str(step_data["id"])] = step_data
                                else:
                                    subval[
                                        self.get_next_iteration(
                                            step_data.get("iteration")
                                        )
                                    ] = step_data

                            dt[k] = subval

                            if len(subval.values()) != len(v):
                                self.raise_parsing_exception(
                                    f"Conversion gave {len(subval.values())} elements instead of {len(v)}"
                                )
                    else:
                        dt[k] = v

                    continue

                raise_parsing_exception(f"Unknown subkeys {subk}")

    def align_properties(self):
        if "created_date" not in self._data and "date" not in self._data:
            self.raise_parsing_exception(
                "Cannot find created_date and date in the document"
            )

        if "declaration_type" not in self._data:
            self.raise_parsing_exception("Cannot find declaration_type in the document")

        if "created_date" in self._data:
            self._data["created_date"] = datetime.fromtimestamp(
                self._data["created_date"]
            ).strftime("%d.%m.%Y %H:%M:%S")
        else:
            self._data["created_date"] = dt_parse(self._data["date"]).strftime(
                "%d.%m.%Y %H:%M:%S"
            )

        self._data["lastmodified_date"] = self._data["created_date"]
        self._data["data"]["step_0"]["declarationType"] = str(
            self._data["declaration_type"]
        )

        if self._data["declaration_type"] == 1:
            self._data["data"]["step_0"]["declarationYear1"] = self._data["data"][
                "step_0"
            ]["declaration_period"]
        elif self._data["declaration_type"] == 2:
            (
                self._data["data"]["step_0"]["declarationYearFrom"],
                self._data["data"]["step_0"]["declarationYearTo"],
            ) = self._data["data"]["step_0"]["declaration_period"].split(" - ")

        elif self._data["declaration_type"] == 3:
            self._data["data"]["step_0"]["declarationYear3"] = self._data["data"][
                "step_0"
            ]["declaration_period"]

        elif self._data["declaration_type"] == 4:
            self._data["data"]["step_0"]["declarationYear4"] = self._data["data"][
                "step_0"
            ]["declaration_period"]


        # TODO: correctly fill other year keys
        #         declarationYear4

        for k, v in self._data["data"].items():
            v = self.apply_boolean_fix(v)

    def convert(self):
        # TODO: form of change
        if self.schema_version == 1:
            return self._data

        self.remove_data_key()
        self.align_properties()

        return self._data


def check_if_empty(s):
    # TODO: validate inclusion of [] in the list
    if s in ("", "[Не відомо]", "[Конфіденційна інформація]", "[Не застосовується]", []):
        return True

    return False


def strip_empty_elements(doc):
    if isinstance(doc, list):
        doc = [strip_empty_elements(d) for d in doc if not check_if_empty(d)]

    if isinstance(doc, dict):
        doc = {
            k: strip_empty_elements(v) for k, v in doc.items() if not check_if_empty(v)
        }

    return doc


if __name__ == '__main__':
    dc = DeclarationConverter(
        "converter_data/dump/2be988d5-e2ac-4009-a291-1edfef9de11c.json"
    )
    res = dc.convert()

    with open("/Users/dchaplinsky/Downloads/test_output_stripped.json", "w") as fp:
        json.dump(
            strip_empty_elements(res), fp, ensure_ascii=False, indent=4, sort_keys=True
        )