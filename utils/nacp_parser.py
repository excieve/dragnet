import re
import json
import os.path
import jmespath
import logging

from string import capwords
from parsel import Selector
from dateutil.parser import parse as dt_parse

from names_translator.name_utils import generate_all_names, autocomplete_suggestions, concat_name, title, parse_fullname
from new_format_converter import DeclarationConverter

logger = logging.getLogger("dragnet.nacp_parser")


class BadJSONData(Exception):
    pass


class BadHTMLData(Exception):
    pass


def parse_guid_from_fname(json_fname):
    m = re.search(r"([0-9\-a-z]{36})", os.path.basename(json_fname))

    if m:
        return m.group(1), json_fname
    else:
        return False


def is_cyr(name):
    return re.search(r"[а-яіїєґ]+", name.lower(), re.UNICODE) is not None


def is_ukr(name):
    return re.search(r"['іїєґ]+", name.lower(), re.UNICODE) is not None


def replace_apostrophes(s):
    return s.replace("`", "'").replace("’", "'")


def replace_arg(request, key, value):
    args = request.GET.copy()
    args[key] = value
    return args.urlencode()


def concat_fields(resp, fields):
    out = list()
    for f in fields:
        res = f.search(resp)
        if not isinstance(res, (list, tuple, dict)):
            res = [res]
        out.extend(res)
    return " ".join(map(str, out))


def keyword_for_sorting(keyword, maxlen=40):
    if is_cyr(keyword):
        keyword = keyword.upper().replace("I", "І")
    return keyword.upper().replace("Є", "ЖЄ").replace("І", "ЙІ").replace("Ї", "ЙЇ")[:maxlen]


class NacpDeclarationParser(object):
    # TODO: Some of these are declarations.com.ua only maps and probably should be moved there
    declaration_types = {"1": "Щорічна", "2": "Перед звільненням", "3": "Після звільнення", "4": "Кандидата на посаду"}
    types = {
        "1": "Декларація",
        "2": "Повідомлення про суттєві зміни в майновому стані",
        "3": "Виправлена декларація",
        "4": "Повідомлення про відкриття валютного рахунка",
    }

    region_types = {
        "1.2.1": "Кримська Автономна Республіка",
        "1.2.5": "Вінницька область",
        "1.2.7": "Волинська область",
        "1.2.12": "Дніпропетровська область",
        "1.2.14": "Донецька область",
        "1.2.18": "Житомирська область",
        "1.2.21": "Закарпатська область",
        "1.2.23": "Запорізька область",
        "1.2.26": "Івано-Франківська область",
        "1.2.80": "м. Київ",
        "1.2.32": "Київська область",
        "1.2.35": "Кіровоградська область",
        "1.2.46": "Львівська область",
        "1.2.44": "Луганська область",
        "1.2.48": "Миколаївська область",
        "1.2.51": "Одеська область",
        "1.2.53": "Полтавська область",
        "1.2.56": "Рівненська область",
        "1.2.85": "Севастополь",
        "1.2.59": "Сумська область",
        "1.2.61": "Тернопільська область",
        "1.2.63": "Харківська область",
        "1.2.65": "Херсонська область",
        "1.2.68": "Хмельницька область",
        "1.2.71": "Черкаська область",
        "1.2.73": "Чернівецька область",
        "1.2.74": "Чернігівська область",
    }

    region_regexps = [
        (r"автономн(?:а|ая|ої|ой) республ[и|і]к[а|и] кр[и|ы]м", "Кримська Автономна Республіка"),
        (r"^севастополь / укра[ї|и]на$", "Кримська Автономна Республіка"),
        (r"^севастополь$", "Кримська Автономна Республіка"),
        (r"^с[и|і]мферополь / укра[ї|и]на$", "Кримська Автономна Республіка"),
        (r"^с[и|і]мферополь$", "Кримська Автономна Республіка"),
        (r"в[і|и]нниць?к(?:а|ая|ої|ой) обл", "Вінницька область"),
        (r"^в[і|и]нниц[а|я] / укра[ї|и]на$", "Вінницька область"),
        (r"^в[і|и]нниц[а|я]$", "Вінницька область"),
        (r"вол[и|ы]нсь?к(?:а|ої|ая|ой) обл", "Волинська область"),
        (r"^луць?к / укра[ї|и]на$", "Волинська область"),
        (r"^луць?к$", "Волинська область"),
        (r"дн[і|е]про(?:петро)?всь?к(?:а|ої|ая|ой) обл", "Дніпропетровська область"),
        (r"^дн[і|е]про(?:петро)?всь?к / укра[и|ї]на$", "Дніпропетровська область"),
        (r"^дн[і|е]про(?:петро)?всь?к$", "Дніпропетровська область"),
        (r"^дн[і|е]про?$", "Дніпропетровська область"),
        (r"донець?к(?:а|ої|ая|ой) обл", "Донецька область"),
        (r"^донець?к / укра[и|ї]на$", "Донецька область"),
        (r"^донець?к$", "Донецька область"),
        (r"житомирсь?к(?:а|ої|ая|ой) обл", "Житомирська область"),
        (r"^житомир / укра[и|ї]на$", "Житомирська область"),
        (r"^житомир$", "Житомирська область"),
        (r"закарпатсь?к(?:а|ої|ая|ой) обл", "Закарпатська область"),
        (r"^ужгород / укра[и|ї]на$", "Закарпатська область"),
        (r"^ужгород$", "Закарпатська область"),
        (r"запор(?:ізьк|ожск)(?:а|ої|ая|ой) обл", "Запорізька область"),
        (r"^(?:запоріжжя|запорожье) / укра[и|ї]на$", "Запорізька область"),
        (r"^запоріжжя|запорожье$", "Запорізька область"),
        (r"франк[і|о]всь?к(?:а|ої|ая|ой) обл", "Івано-Франківська область"),
        (r"^[і|и]вано-франк[і|о]всь?к / укра[и|ї]на$", "Івано-Франківська область"),
        (r"^[і|и]вано-франк[і|о]всь?к$", "Івано-Франківська область"),
        (r"ки[ї|е]всь?к(?:а|ої|ая|ой) обл", "Київська область"),
        (r"бровари", "Київська область"),
        (r"^ки[ї|е]всь?ка область/ки[ї|е]в / укра[и|ї]на$", "м. Київ"),
        (r"^ки[ї|е]в / укра[и|ї]на$", "м. Київ"),
        (r"^ки[ї|е]в$", "м. Київ"),
        (r"^м[і|и]сто ки[ї|е]в$", "м. Київ"),
        (r"к[і|и]ровоградсь?к(?:а|ої|ая|ой) обл", "Кіровоградська область"),
        (r"кропивниць?к(?:а|ої|ая|ой) обл", "Кіровоградська область"),
        (r"^к[і|и]ровоград / укра[и|ї]на$", "Кіровоградська область"),
        (r"^к[і|и]ровоград$", "Кіровоградська область"),
        (r"^кропивниць?кий / укра[и|ї]на$", "Кіровоградська область"),
        (r"лугансь?к(?:а|ої|ая|ой) обл", "Луганська область"),
        (r"^лугансь?к / укра[и|ї]на$", "Луганська область"),
        (r"^лугансь?к$", "Луганська область"),
        (r"льв[і|о]всь?к(?:а|ої|ая|ой) обл", "Львівська область"),
        (r"^льв[і|о]в / укра[и|ї]на$", "Львівська область"),
        (r"^льв[і|о]в$", "Львівська область"),
        (r"[м|н]икола[ї|е]всь?к(?:а|ої|ая|ой) обл", "Миколаївська область"),
        (r"^[м|н]икола[ї|е]в / укра[и|ї]на$", "Миколаївська область"),
        (r"^[м|н]икола[ї|е]в$", "Миколаївська область"),
        (r"одес[с|ь]к(?:а|ої|ая|ой) обл", "Одеська область"),
        (r"^одесс?а / укра[и|ї]на$", "Одеська область"),
        (r"^одесс?а$", "Одеська область"),
        (r"полтавсь?к(?:а|ої|ая|ой) обл", "Полтавська область"),
        (r"^полтава / укра[и|ї]на$", "Полтавська область"),
        (r"^полтава$", "Полтавська область"),
        (r"р[і|о]вненсь?к(?:а|ої|ая|ой) обл", "Рівненська область"),
        (r"^р[і|о]вн[е|о] / укра[и|ї]на$", "Рівненська область"),
        (r"^р[і|о]вн[е|о]$", "Рівненська область"),
        (r"сумсь?к(?:а|ої|ая|ой) обл", "Сумська область"),
        (r"^сум[и|ы] / укра[и|ї]на$", "Сумська область"),
        (r"^сум[и|ы]$", "Сумська область"),
        (r"терноп[і|о]льсь?к(?:а|ої|ая|ой) обл", "Тернопільська область"),
        (r"^терноп[і|о]ль / укра[и|ї]на$", "Тернопільська область"),
        (r"^терноп[і|о]ль$", "Тернопільська область"),
        (r"харь?к[і|о]всь?к(?:а|ої|ая|ой) обл", "Харківська область"),
        (r"^харь?к[і|о]в / укра[и|ї]на$", "Харківська область"),
        (r"^харь?к[і|о]в$", "Харківська область"),
        (r"херсонсь?к(?:а|ої|ая|ой) обл", "Херсонська область"),
        (r"^херсон / укра[и|ї]на$", "Херсонська область"),
        (r"^херсон$", "Херсонська область"),
        (r"хмельниць?к(?:а|ої|ая|ой) обл", "Хмельницька область"),
        (r"^хмельниць?кий / укра[и|ї]на$", "Хмельницька область"),
        (r"^хмельниць?кий$", "Хмельницька область"),
        (r"черкас[ь|с]к(?:а|ої|ая|ой) обл", "Черкаська область"),
        (r"^черкас(?:и|сы) / укра[и|ї]на$", "Черкаська область"),
        (r"^черкас(?:и|сы)$", "Черкаська область"),
        (r"черн[і|о]в[е|и]ць?к(?:а|ої|ая|ой) обл", "Чернівецька область"),
        (r"^черн[і|о]вц[і|ы] / укра[и|ї]на$", "Чернівецька область"),
        (r"^черн[і|о]вц[і|ы]$", "Чернівецька область"),
        (r"черн[і|и]г[і|о]всь?к(?:а|ої|ая|ой) обл", "Чернігівська область"),
        (r"^черн[і|и]г[і|о]в / укра[и|ї]на$", "Чернігівська область"),
        (r"^черн[і|и]г[і|о]в$", "Чернігівська область"),
    ]

    dangerous_chunks = ["onchange", "onclick", "onmouseover", "onmouseout", "onkeydown", "onload", "<img", "<scri"]

    INDEX_CARD_FIELDS = [
        jmespath.compile("general.last_name"),
        jmespath.compile("general.name"),
        jmespath.compile("general.patronymic"),
        jmespath.compile("general.full_name"),
        jmespath.compile("general.post.post"),
        jmespath.compile("general.post.office"),
        jmespath.compile("general.post.region"),
        jmespath.compile("general.post.actual_region"),
        jmespath.compile("intro.declaration_year"),
        jmespath.compile("intro.doc_type"),
        jmespath.compile("declaration.source"),
        jmespath.compile("declaration.url"),
    ]

    names_paths = [
        jmespath.compile("step_1.[lastname,firstname,middlename]"),
        jmespath.compile("step_1.[previous_lastname,previous_firstname,previous_middlename]"),
        jmespath.compile("step_2.*.[lastname,firstname,middlename]"),
        jmespath.compile("step_2.*.[previous_lastname,previous_firstname,previous_middlename]"),
        jmespath.compile("step_2.*.[source_ua_lastname,source_ua_firstname,source_ua_middlename]"),
        jmespath.compile("step_3.*.rights[].*.[ua_lastname,ua_firstname,ua_middlename][]"),
        jmespath.compile("step_3.*.rights[].*.ukr_fullname[]"),
        jmespath.compile("step_4.*.rights[].*.[ua_lastname,ua_firstname,ua_middlename][]"),
        jmespath.compile("step_4.*.[addition_lastname,addition_firstname,addition_middlename]"),
        jmespath.compile("step_6.*.rights[].*.[ua_lastname,ua_firstname,ua_middlename][]"),
        jmespath.compile("step_6.*.rights[].*.[ukr_lastname,ukr_firstname,ukr_middlename][]"),
        jmespath.compile("step_6.*.rights[].*.[ukr_fullname][]"),
        jmespath.compile("step_7.*.rights[].*.[ua_lastname,ua_firstname,ua_middlename][]"),
        jmespath.compile("step_8.*.rights[].*.[ua_lastname,ua_firstname,ua_middlename][]"),
        jmespath.compile("step_10.*.rights[].*.[ua_lastname,ua_firstname,ua_middlename][]"),
        jmespath.compile("step_11.*.rights[].*.[ua_lastname,ua_firstname,ua_middlename][]"),
        jmespath.compile("step_11.*.rights[].*.ukr_fullname[]"),
        jmespath.compile("step_11.*.rights[].*.[source_ua_lastname,source_ua_firstname,source_ua_middlename][]"),
        jmespath.compile("step_11.*.source_ukr_fullname"),
        jmespath.compile("step_12.*.[debtor_ua_lastname,debtor_ua_firstname,debtor_ua_middlename]"),
        jmespath.compile("step_12.*.rights[].*.[ua_lastname,ua_firstname,ua_middlename][]"),
        jmespath.compile("step_13.*.[emitent_ua_lastname,emitent_ua_firstname,emitent_ua_middlename]"),
        jmespath.compile("step_13.*.emitent_ukr_fullname"),
        jmespath.compile(
            "step_13.*.guarantor[].*.[guarantor_ua_lastname,guarantor_ua_firstname,guarantor_ua_middlename][]"
        ),
        jmespath.compile(
            "step_13.*.guarantor_realty[].*.[realty_rights_ua_lastname,realty_rights_ua_firstname,realty_rights_ua_middlename][]"
        ),
        jmespath.compile("step_15.*.[emitent_ua_lastname,emitent_ua_firstname,emitent_ua_middlename]"),
    ]

    corrected = set()
    translator = None

    @staticmethod
    def parse_date(s):
        return dt_parse(s, dayfirst=True)

    @classmethod
    def extract_textual_data(cls, decl):
        res = decl.css("*:not(td)>span.block::text, *:not(td)>span.border::text, td *::text").extract()

        res += decl.css(
            "fieldset:contains('Зареєстроване місце проживання') .person-info:contains('Місто')::text"
        ).extract()

        res = filter(None, map(lambda x: x.strip().strip("\xa0"), res))
        res = filter(lambda x: not x.endswith(":"), res)
        res = filter(lambda x: not x.startswith("["), res)
        res = filter(lambda x: not x.endswith("]"), res)

        # Very special case
        res = list(filter(lambda x: not x.startswith("Загальна площа (м"), res))
        res_en = []

        if cls.translator is not None:
            res_en = [cls.translator.translate(x)["translation"] for x in res]

        return res + res_en

    @staticmethod
    def extract_obj_ids(decl_data):
        objs = set()

        for v in decl_data.values():
            if isinstance(v, dict):
                for k in v.keys():
                    if k.isdigit():
                        objs.add(k)
        return list(objs)

    @classmethod
    def decode_region(cls, region_html):
        if len(region_html) > 2:
            for pattern, region in cls.region_regexps:
                if re.search(pattern, region_html.lower().replace("м.", "").strip()):
                    return region
        return ""

    @classmethod
    def _parse_me(cls, base_fname):
        json_fname = "{}.json".format(base_fname)
        html_fname = "{}.html".format(base_fname)
        resp = {"intro": {}, "declaration": {}}

        try:
            with open(json_fname, "r") as fp:
                data = json.load(fp)

            with open(html_fname, "r") as fp:
                raw_html = fp.read()
                html = Selector(raw_html)
        except ValueError:
            logger.error("File {} or it's HTML counterpart cannot be parsed".format(json_fname))
            return None
        except FileNotFoundError:
            logger.error("File {} or it's HTML counterpart cannot be found".format(json_fname))
            return None

        id_ = data.get("id")
        created_date = data.get("created_date")
        user_declarant_id = data.get("user_declarant_id")

        raw_html_lowered = raw_html.lower()
        for chunk in cls.dangerous_chunks:
            if chunk in raw_html_lowered:
                raise BadHTMLData("Dangerous fragment found: {}, {}".format(id_, base_fname))

        try:
            data = data["data"]
        except KeyError:
            raise BadJSONData("API brainfart: {}, {}".format(id_, base_fname))

        if "step_0" not in data:
            raise BadJSONData("Bad header format: {}, {}".format(id_, base_fname))

        resp["doc_uuid"] = "nacp_{}".format(id_)
        resp["ft_src"] = "\n".join(cls.extract_textual_data(html))
        resp["obj_ids"] = cls.extract_obj_ids(data)

        resp["nacp_orig"] = data
        resp["declaration"]["url"] = "https://public.nazk.gov.ua/documents/{}".format(id_)
        resp["declaration"]["source"] = "NACP"
        resp["declaration"]["basename"] = os.path.basename(base_fname)

        resp["intro"]["corrected"] = id_ in cls.corrected
        resp["intro"]["date"] = cls.parse_date(created_date).isoformat()
        resp["intro"]["user_declarant_id"] = user_declarant_id

        if "declarationType" not in data["step_0"] or "changesYear" in data["step_0"]:
            resp["intro"]["doc_type"] = "Форма змін"

            if "changesYear" in data["step_0"]:
                resp["intro"]["declaration_year"] = int(data["step_0"]["changesYear"])
        else:
            resp["intro"]["doc_type"] = cls.declaration_types[data["step_0"]["declarationType"]]
            if "declarationYearTo" in data["step_0"]:
                resp["intro"]["declaration_year_to"] = str(cls.parse_date(data["step_0"]["declarationYearTo"]).year)

            if "declarationYearFrom" in data["step_0"]:
                decl_year_from_dt = cls.parse_date(data["step_0"]["declarationYearFrom"]).year
                resp["intro"]["declaration_year_from"] = str(decl_year_from_dt)
                resp["intro"]["declaration_year"] = decl_year_from_dt

            if "declarationYear1" in data["step_0"]:
                resp["intro"]["declaration_year"] = int(data["step_0"]["declarationYear1"])

            if "declarationYear3" in data["step_0"] and data["step_0"]["declarationYear3"]:
                resp["intro"]["declaration_year"] = int(data["step_0"]["declarationYear3"])

            if "declarationYear4" in data["step_0"] and data["step_0"]["declarationYear4"]:
                resp["intro"]["declaration_year"] = int(data["step_0"]["declarationYear4"])

        resp["general"] = {
            "last_name": replace_apostrophes(title(data["step_1"]["lastname"])),
            "name": replace_apostrophes(title(data["step_1"]["firstname"])),
            "patronymic": replace_apostrophes(title(data["step_1"].get("middlename", ""))),
            "full_name": replace_apostrophes(
                "{} {} {}".format(
                    title(data["step_1"]["lastname"]),
                    title(data["step_1"]["firstname"]),
                    title(data["step_1"].get("middlename", "")),
                )
            ),
            "post": {
                "post": replace_apostrophes(data["step_1"].get("workPost", "")),
                "post_type": replace_apostrophes(data["step_1"].get("postType", "")),
                "office": replace_apostrophes(data["step_1"].get("workPlace", "")),
                "actual_region": replace_apostrophes(cls.region_types.get(data["step_1"].get("actual_region", ""), "")),
                "region": replace_apostrophes(cls.region_types.get(data["step_1"].get("region", ""), "")),
            },
        }

        # Let's extract all names for the autocomplete and search
        extracted_names = []
        persons = set()
        names_autocomplete = set()

        # Extracting all persons mentioned in different sections of that declaration
        for pth in cls.names_paths:
            res = pth.search(data)
            if res:
                if isinstance(res[0], str):
                    if len(res) == 1 and res[0]:
                        l, f, p, _ = parse_fullname(res[0])
                        res = [l, f, p]
                    res = [res]

                if res[0] is None:
                    res = [res]

                res = [r for r in res if all(map(bool, r))]
                for name in res:
                    # assuming fully parsed name here
                    if len(name) == 3:
                        extracted_names.append(name)
                    else:
                        found_as_name = False
                        for chunk in name:
                            l, f, p, _ = parse_fullname(chunk)
                            if f:
                                found_as_name = True
                                extracted_names.append([l, f, p])

                        if not found_as_name and len(name) == 2:
                            extracted_names.append([name[0], name[1], ""])

        for name in extracted_names:
            persons |= generate_all_names(name[0], name[1], name[2])

            names_autocomplete |= autocomplete_suggestions(concat_name(*name))

        if "step_2" in data:
            family = data["step_2"]

            if isinstance(family, dict):
                resp["general"]["family"] = []

                for member in family.values():
                    if not isinstance(member, dict):
                        continue

                    name = member.get("ukr_full_name", "")
                    if not name:
                        name = "{} {} {}".format(
                            title(member.get("lastname", "")),
                            title(member.get("firstname", "")),
                            title(member.get("middlename", "")),
                        )

                    resp["general"]["family"].append(
                        {"family_name": replace_apostrophes(name), "relations": member.get("subjectRelation", "")}
                    )

        # get regions from estate list
        if "step_3" in data and isinstance(data["step_3"], dict) and data["step_3"]:
            if "estate" not in resp:
                resp["estate"] = []
            for estate in data["step_3"].values():
                if isinstance(estate, dict) and "region" in estate:
                    region = replace_apostrophes(cls.region_types.get(estate.get("region", ""), ""))
                    if region:
                        resp["estate"].append({"region": region})

        if "step_4" in data and isinstance(data["step_4"], dict) and data["step_4"]:
            if "estate" not in resp:
                resp["estate"] = []
            for estate in data["step_4"].values():
                if isinstance(estate, dict) and "region" in estate:
                    region = replace_apostrophes(cls.region_types.get(estate.get("region", ""), ""))
                    if region:
                        resp["estate"].append({"region": region})

        if "estate" in resp:
            estate_list = html.css(
                "table:contains('Місцезнаходження') td:contains('Населений пункт') span::text"
            ).extract()

            for estate in estate_list:
                region = cls.decode_region(estate)
                if region:
                    resp["estate"].append({"region": region})

        resp["general"]["full_name_suggest"] = [
            {"input": resp["general"]["full_name"], "weight": 5},
            {
                "input": " ".join(
                    [resp["general"]["name"], resp["general"]["patronymic"], resp["general"]["last_name"]]
                ),
                "weight": 3,
            },
            {"input": " ".join([resp["general"]["name"], resp["general"]["last_name"]]), "weight": 3},
        ]

        resp["general"]["full_name_for_sorting"] = keyword_for_sorting(resp["general"]["full_name"])

        if not resp["general"]["post"]["region"]:
            region_html = html.css(
                "fieldset:contains('Зареєстроване місце проживання') .person-info:contains('Місто')::text"
            ).extract()

            if len(region_html) > 1 and region_html[1].strip():
                resp["general"]["post"]["region"] = cls.decode_region(region_html[1])
            else:
                region_html = html.css(
                    "fieldset:contains('Зареєстроване місце проживання') .person-info:contains('Місто') span::text"
                ).extract()

                if region_html and region_html[0]:
                    resp["general"]["post"]["region"] = cls.decode_region(region_html[0])

        if not resp["general"]["post"]["actual_region"]:
            region_html = html.css(
                "fieldset:contains('Місце фактичного проживання') .person-info:contains('Місто')::text"
            ).extract()

            if len(region_html) > 1 and region_html[1].strip():
                resp["general"]["post"]["actual_region"] = cls.decode_region(region_html[1])
            else:
                region_html = html.css(
                    "fieldset:contains('Місце фактичного проживання') .person-info:contains('Місто') span::text"
                ).extract()

                if region_html and region_html[0]:
                    resp["general"]["post"]["actual_region"] = cls.decode_region(region_html[0])

        # if set only one region use it value for second one
        if not resp["general"]["post"]["actual_region"] and resp["general"]["post"]["region"]:
            resp["general"]["post"]["actual_region"] = resp["general"]["post"]["region"]
        elif not resp["general"]["post"]["region"] and resp["general"]["post"]["actual_region"]:
            resp["general"]["post"]["region"] = resp["general"]["post"]["actual_region"]

        resp["index_card"] = concat_fields(resp, cls.INDEX_CARD_FIELDS)

        resp["persons"] = list(filter(None, persons))
        resp["names_autocomplete"] = list(filter(None, names_autocomplete))

        return resp

    @classmethod
    def parse(cls, fname):
        try:
            return cls._parse_me(fname.replace(".json", ""))
        except (BadJSONData, BadHTMLData, ValueError) as e:
            logger.error("{}: on file {}".format(e, fname))
            return None


class NacpDeclarationNewFormatParser(NacpDeclarationParser):
    @classmethod
    def dict_generator(cls, indict, pre=None):
        pre = pre[:] if pre else []
        if isinstance(indict, dict):
            for key, value in indict.items():
                if isinstance(value, dict):
                    for d in cls.dict_generator(value, [key] + pre):
                        yield d
                elif isinstance(value, (list, tuple)):
                    for v in value:
                        for d in cls.dict_generator(v, [key] + pre):
                            yield d
                else:
                    yield value
        else:
            yield indict

    @classmethod
    def filter_only_interesting(cls, src):
        def inner_filter(val):
            if isinstance(val, (int, float)) and str(val) not in ["0", "1"]:
                return True

            if (
                isinstance(val, str)
                and val
                and val.lower()
                not in [
                    "uah",
                    "м²",
                    "usd",
                    "0",
                    "1",
                    "",
                    "грн",
                    "eur",
                    "[не відомо]",
                    "[конфіденційна інформація]",
                    "[не застосовується]",
                    "га",
                    "місто",
                    "j",
                    "no",
                    "ні",
                    "true",
                    "false",
                    "у суб'єкта декларування відсутні об'єкти для декларування в цьому розділі.",
                ]
                and not val.startswith("http")
            ):
                return True

            return False

        return list(
            map(
                str,
                filter(
                    inner_filter,
                    cls.dict_generator(src),
                ),
            )
        )

    @classmethod
    def extract_textual_data_from_json(cls, decl):
        res = cls.filter_only_interesting(decl)
        res_en = []

        if cls.translator is not None:
            res_en = [cls.translator.translate(x)["translation"] for x in res]

        return res + res_en

    @classmethod
    def _resolve_region(cls, region):
        if not region.strip():
            return None

        if re.search(r"^україна$", region.lower().strip()):
            return None

        for chunk in map(str.strip, region.split("/")):
            for pattern, clean_region in cls.region_regexps:
                if re.search(pattern, chunk.lower().replace("м.", "").strip()):
                    return replace_apostrophes(clean_region)

        logger.warning(f"Cannot match the region {region} to the list of known regions")

    @classmethod
    def _parse_me(cls, base_fname):
        json_fname = "{}.json".format(base_fname)
        resp = {"intro": {}, "declaration": {}}

        try:
            converter = DeclarationConverter(json_fname)
            data = converter.convert()
        except (ValueError, FileNotFoundError) as e:
            logger.error("File {} or it's HTML counterpart cannot be found".format(json_fname))
            return None

        id_ = data.get("id")
        type_ = data.get("type")
        created_date = data.get("created_date")
        user_declarant_id = data.get("user_declarant_id")

        for k in [
            "corruption_affected",
            "post_category",
            "post_type",
            "responsible_position",
            "schema_version",
            "type",
        ]:
            if k in data:
                resp["intro"]["nacp_" + k] = data[k]

        try:
            data = data["data"]
        except KeyError:
            raise BadJSONData("API brainfart: {}, {}".format(id_, base_fname))

        if "step_0" not in data:
            raise BadJSONData("Bad header format: {}, {}".format(id_, base_fname))

        resp["doc_uuid"] = "nacp_{}".format(id_)
        resp["ft_src"] = "\n".join(cls.extract_textual_data_from_json(data))
        resp["obj_ids"] = cls.extract_obj_ids(data)

        resp["nacp_orig"] = data
        resp["declaration"]["url"] = "https://public.nazk.gov.ua/documents/{}".format(id_)
        resp["declaration"]["source"] = "NACP"
        resp["declaration"]["basename"] = os.path.basename(base_fname)

        if str(type_) == "3":
            resp["intro"]["corrected"] = True
        else:
            resp["intro"]["corrected"] = id_ in cls.corrected

        resp["intro"]["date"] = cls.parse_date(created_date).isoformat()
        resp["intro"]["user_declarant_id"] = user_declarant_id

        if "declarationType" not in data["step_0"] or "changesYear" in data["step_0"]:
            resp["intro"]["doc_type"] = "Форма змін"

            if "changesYear" in data["step_0"]:
                resp["intro"]["declaration_year"] = int(data["step_0"]["changesYear"])
        else:
            resp["intro"]["doc_type"] = cls.declaration_types[data["step_0"]["declarationType"]]
            if "declarationYearTo" in data["step_0"]:
                resp["intro"]["declaration_year_to"] = str(cls.parse_date(data["step_0"]["declarationYearTo"]).year)

            if "declarationYearFrom" in data["step_0"]:
                decl_year_from_dt = cls.parse_date(data["step_0"]["declarationYearFrom"]).year
                resp["intro"]["declaration_year_from"] = str(decl_year_from_dt)
                resp["intro"]["declaration_year"] = decl_year_from_dt

            if "declarationYear1" in data["step_0"]:
                resp["intro"]["declaration_year"] = int(data["step_0"]["declarationYear1"])

            if "declarationYear3" in data["step_0"] and data["step_0"]["declarationYear3"]:
                resp["intro"]["declaration_year"] = int(data["step_0"]["declarationYear3"])

            if "declarationYear4" in data["step_0"] and data["step_0"]["declarationYear4"]:
                resp["intro"]["declaration_year"] = int(data["step_0"]["declarationYear4"])

        resp["general"] = {
            "last_name": replace_apostrophes(title(data["step_1"]["lastname"])),
            "name": replace_apostrophes(title(data["step_1"]["firstname"])),
            "patronymic": replace_apostrophes(title(data["step_1"].get("middlename", ""))),
            "full_name": replace_apostrophes(
                "{} {} {}".format(
                    title(data["step_1"]["lastname"]),
                    title(data["step_1"]["firstname"]),
                    title(data["step_1"].get("middlename", "")),
                )
            ),
            "post": {
                "post": replace_apostrophes(data["step_1"].get("workPost", "")),
                "post_type": replace_apostrophes(data["step_1"].get("postType", "")),
                "office": replace_apostrophes(data["step_1"].get("workPlace", "")),
                "region": cls._resolve_region(data["step_1"].get("cityType", "")) or "",
                "actual_region": cls._resolve_region(data["step_1"].get("actual_cityType", "")) or "",
            },
        }

        # Let's extract all names for the autocomplete and search
        extracted_names = []
        persons = set()
        names_autocomplete = set()

        # Extracting all persons mentioned in different sections of that declaration
        for pth in cls.names_paths:
            res = pth.search(data)
            if res:
                if isinstance(res[0], str):
                    if len(res) == 1 and res[0]:
                        l, f, p, _ = parse_fullname(res[0])
                        res = [l, f, p]
                    res = [res]

                if res[0] is None:
                    res = [res]

                res = [r for r in res if all(map(bool, r))]
                for name in res:
                    # assuming fully parsed name here
                    if len(name) == 3:
                        extracted_names.append(name)
                    else:
                        found_as_name = False
                        for chunk in name:
                            l, f, p, _ = parse_fullname(chunk)
                            if f:
                                found_as_name = True
                                extracted_names.append([l, f, p])

                        if not found_as_name and len(name) == 2:
                            extracted_names.append([name[0], name[1], ""])

        for name in extracted_names:
            persons |= generate_all_names(name[0], name[1], name[2])

            names_autocomplete |= autocomplete_suggestions(concat_name(*name))

        if "step_2" in data:
            family = data["step_2"]

            if isinstance(family, dict):
                resp["general"]["family"] = []

                for member in family.values():
                    if not isinstance(member, dict):
                        continue

                    name = member.get("ukr_full_name", "")
                    if not name:
                        name = "{} {} {}".format(
                            title(member.get("lastname", "")),
                            title(member.get("firstname", "")),
                            title(member.get("middlename", "")),
                        )

                    resp["general"]["family"].append(
                        {"family_name": replace_apostrophes(name), "relations": member.get("subjectRelation", "")}
                    )

        # if set only one region use it value for second one
        if not resp["general"]["post"]["actual_region"] and resp["general"]["post"]["region"]:
            resp["general"]["post"]["actual_region"] = resp["general"]["post"]["region"]
        elif not resp["general"]["post"]["region"] and resp["general"]["post"]["actual_region"]:
            resp["general"]["post"]["region"] = resp["general"]["post"]["actual_region"]

        resp["estate"] = []
        if resp["general"]["post"]["region"]:
            resp["estate"].append({"region": resp["general"]["post"]["region"]})

        if resp["general"]["post"]["actual_region"]:
            resp["estate"].append({"region": resp["general"]["post"]["actual_region"]})

        # get regions from estate list
        for step in ["step_3", "step_4"]:
            if step in data and isinstance(data[step], dict) and data[step]:
                for estate in data[step].values():
                    if isinstance(estate, dict) and "ua_cityType" in estate:
                        region = cls._resolve_region(estate.get("ua_cityType", ""))
                        if region:
                            resp["estate"].append({"region": region})

        resp["general"]["full_name_suggest"] = [
            {"input": resp["general"]["full_name"], "weight": 5},
            {
                "input": " ".join(
                    [resp["general"]["name"], resp["general"]["patronymic"], resp["general"]["last_name"]]
                ),
                "weight": 3,
            },
            {"input": " ".join([resp["general"]["name"], resp["general"]["last_name"]]), "weight": 3},
        ]

        resp["general"]["full_name_for_sorting"] = keyword_for_sorting(resp["general"]["full_name"])

        resp["index_card"] = concat_fields(resp, cls.INDEX_CARD_FIELDS)

        resp["persons"] = list(filter(None, persons))
        resp["names_autocomplete"] = list(filter(None, names_autocomplete))

        return resp


if __name__ == "__main__":

    import sys, os, os.path

    sys.path = [os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../declarations_site")] + sys.path
    os.environ["DJANGO_SETTINGS_MODULE"] = "declarations_site.settings"

    import django

    django.setup()
    from catalog.translator import Translator

    def json_dump(d):
        return json.dumps(d, ensure_ascii=False, indent=4, sort_keys=True)

    translator = Translator()
    translator.fetch_full_dict_from_db()
    NacpDeclarationParser.translator = translator
    NacpDeclarationNewFormatParser.translator = translator

    res = NacpDeclarationNewFormatParser.parse(
        "/Users/dchaplinsky/Projects/declarations/declarations.com.ua/converter_data/dump/2876a5ef-e48d-40f0-8fb2-296a0a9a4dc5.json"
    )

    # res = NacpDeclarationParser.parse(
    #     "/Users/dchaplinsky/Projects/declarations/declarations.com.ua/converter_data/old/2876a5ef-e48d-40f0-8fb2-296a0a9a4dc5.json"
    # )
    print(json_dump(res))
