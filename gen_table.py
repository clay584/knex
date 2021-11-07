#!/usr/bin/env python3
from itertools import zip_longest
from pytablewriter import MarkdownTableWriter
import re


EMOJI_CHECK = ":heavy_check_mark:"
EMOJI_X = ":x:"
DOCS_URL = "https://clay584.github.io/knex/parsers-reference/#knex.parsers."

PARSERS = sorted(
    [
        {"name": "Append", "type": "General", "status": "implemented"},
        {"name": "Count", "type": "General", "status": "implemented"},
        {"name": "FirstElement", "type": "General", "status": "implemented"},
        {"name": "GetField", "type": "General", "status": "implemented"},
        {"name": "GetIndex", "type": "General", "status": "implemented"},
        {"name": "If-Then-Else", "type": "General", "status": "planned"},
        {"name": "Join", "type": "General", "status": "implemented"},
        {"name": "Jq", "type": "General", "status": "planned"},
        {"name": "JsonToTable", "type": "General", "status": "planned"},
        {"name": "LastElement", "type": "General", "status": "implemented"},
        {"name": "ReverseList", "type": "General", "status": "planned"},
        {"name": "SetIfEmpty", "type": "General", "status": "planned"},
        {"name": "Slice", "type": "General", "status": "planned"},
        {"name": "Sort", "type": "General", "status": "planned"},
        {"name": "Stringify", "type": "General", "status": "planned"},
        {"name": "Unique", "type": "General", "status": "planned"},
        {"name": "WhereFieldEquals", "type": "General", "status": "planned"},
        {"name": "Base64Decode", "type": "String", "status": "implemented"},
        {"name": "Base64Encode", "type": "String", "status": "implemented"},
        {"name": "Concat", "type": "String", "status": "implemented"},
        {"name": "Cut", "type": "String", "status": "planned"},
        {"name": "DumpJSON", "type": "String", "status": "planned"},
        {"name": "FromString", "type": "String", "status": "planned"},
        {"name": "JSONUnescape", "type": "String", "status": "planned"},
        {"name": "Length", "type": "String", "status": "implemented"},
        {"name": "LoadJSON", "type": "String", "status": "planned"},
        {"name": "RegexExtractAll", "type": "String", "status": "implemented"},
        {"name": "RegexReplace", "type": "String", "status": "planned"},
        {"name": "Split", "type": "String", "status": "implemented"},
        {"name": "Substring", "type": "String", "status": "planned"},
        {"name": "ToLower", "type": "String", "status": "implemented"},
        {"name": "ToString", "type": "String", "status": "planned"},
        {"name": "ToUpper", "type": "String", "status": "implemented"},
        {"name": "Trim", "type": "String", "status": "planned"},
        {"name": "Absolute", "type": "Number", "status": "planned"},
        {"name": "Add", "type": "Number", "status": "planned"},
        {"name": "Ceil", "type": "Number", "status": "planned"},
        {"name": "Divide", "type": "Number", "status": "planned"},
        {"name": "Floor", "type": "Number", "status": "planned"},
        {"name": "Modulus", "type": "Number", "status": "planned"},
        {"name": "Multiply", "type": "Number", "status": "planned"},
        {"name": "Round", "type": "Number", "status": "planned"},
        {"name": "Subtract", "type": "Number", "status": "planned"},
        {"name": "SumList", "type": "Number", "status": "planned"},
        {"name": "ToPercent", "type": "Number", "status": "planned"},
        {"name": "BetweenDates", "type": "Date", "status": "planned"},
        {"name": "BetweenHours", "type": "Date", "status": "planned"},
        {"name": "DateStringToISOFormat", "type": "Date", "status": "planned"},
        {"name": "DateToEpoch", "type": "Date", "status": "planned"},
        {"name": "DateToString", "type": "Date", "status": "planned"},
        {"name": "FormattedDateToEpoch", "type": "Date", "status": "planned"},
        {"name": "ModifyDateTime", "type": "Date", "status": "planned"},
        {"name": "TimeStampToDate", "type": "Date", "status": "planned"},
        {"name": "TextFSMParse", "type": "Other", "status": "implemented"},
        {"name": "ThisOrThat", "type": "Other", "status": "planned"},
        {"name": "Ttp", "type": "Other", "status": "planned"},
        {"name": "URLDecode", "type": "Other", "status": "planned"},
        {"name": "URLEncode", "type": "Other", "status": "planned"},
        {"name": "MacAddress", "type": "Other", "status": "implemented"},
        {"name": "PythonFunction", "type": "Other", "status": "planned"},
        {"name": "TemplateRender", "type": "String", "status": "planned"},
        {"name": "Jinja2Render", "type": "String", "status": "planned"},
        {"name": "YamlLoads", "type": "String", "status": "planned"},
        {"name": "YamlDumps", "type": "String", "status": "planned"},
        {"name": "YamaleValidate", "type": "Other", "status": "planned"},
        {"name": "JsonSchemaValidate", "type": "Other", "status": "planned"},
        {"name": "GenieParse", "type": "String", "status": "planned"},
        {"name": "AsnToInt", "type": "Other", "status": "planned"},
        {"name": "ValidateCiscoType5", "type": "Other", "status": "planned"},
        {"name": "NormalInterfaceName", "type": "Other", "status": "planned"},
        {"name": "InterfaceRangeExpand", "type": "Other", "status": "planned"},
        {"name": "SortInterfaceList", "type": "Other", "status": "planned"},
        {"name": "ValidateCiscoType7", "type": "Other", "status": "planned"},
        {"name": "DecodeCiscoType7", "type": "Other", "status": "planned"},
        {"name": "EncodeCiscoType7", "type": "Other", "status": "planned"},
        {"name": "EncryptCiscoType5", "type": "Other", "status": "planned"},
        {"name": "IpProtocolNumberToName", "type": "Other", "status": "planned"},
        {"name": "IpProtocolNameToNumber", "type": "Other", "status": "planned"},
        {"name": "VlanConfigToList", "type": "Other", "status": "planned"},
        {"name": "ToCamelCase", "type": "Other", "status": "planned"},
        {"name": "ToSnakeCase", "type": "Other", "status": "planned"},
        {"name": "Random", "type": "Other", "status": "planned"},
        {"name": "FuzzyWuzzyFind", "type": "Other", "status": "planned"},
        {"name": "IndexOf", "type": "General", "status": "implemented"},
    ],
    key=lambda k: k["name"],
)


def build_field(parser):
    status = EMOJI_CHECK if parser.get("status") == "implemented" else EMOJI_X
    if parser.get("status") == "implemented":
        parser[
            "rendered"
        ] = f"{status} [{parser.get('name')}]({DOCS_URL}{parser.get('name')})"
    else:
        parser["rendered"] = f"{status} {parser.get('name')}"

    return parser


def build_table(data):
    writer = MarkdownTableWriter(
        headers=["General", "String", "Number", "Date", "Other"],
        value_matrix=data,
    )
    return writer.dumps(format="github")


if __name__ == "__main__":
    rendered_parsers = [build_field(parser) for parser in PARSERS]
    generals = [
        x.get("rendered") for x in rendered_parsers if x.get("type") == "General"
    ]
    strings = [x.get("rendered") for x in rendered_parsers if x.get("type") == "String"]
    numbers = [x.get("rendered") for x in rendered_parsers if x.get("type") == "Number"]
    dates = [x.get("rendered") for x in rendered_parsers if x.get("type") == "Date"]
    others = [x.get("rendered") for x in rendered_parsers if x.get("type") == "Other"]

    data = list(
        tuple(zip_longest(generals, strings, numbers, dates, others, fillvalue=""))
    )
    data = [list(x) for x in data]

    table = build_table(data)

    table = "<!-- start replace -->\n" + table + "<!-- end replace -->"

    with open("README.md", "r") as f:
        readme_orig = f.read()

    readme_new = re.sub(
        "<!-- start replace -->?(.*?)<!-- end replace -->",
        table,
        readme_orig,
        flags=re.DOTALL,
    )

    with open("README.md", "w") as f:
        f.write(readme_new)
