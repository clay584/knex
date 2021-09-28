# KNEX

<!-- markdownlint-disable MD001 -->
#### Latest Release (v0.3.1)
<!-- markdownlint-enable MD001 -->
Python library for creating chainable data transformers.

[![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/clay584/knex/Pytest/main)](https://github.com/clay584/knex/actions)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/48345d8053824abaab78d5acfadf1c91)](https://www.codacy.com/gh/clay584/knex/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=clay584/knex&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/48345d8053824abaab78d5acfadf1c91)](https://www.codacy.com/gh/clay584/knex/dashboard?utm_source=github.com&utm_medium=referral&utm_content=clay584/knex&utm_campaign=Badge_Coverage)
[![Known Vulnerabilities](https://snyk.io/test/github/clay584/knex/badge.svg)](https://snyk.io/test/github/clay584/knex)
[![GitHub last commit (branch)](https://img.shields.io/github/last-commit/clay584/knex/main)](https://github.com/clay584/knex/commits/main)

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/knex)

[![PyPI](https://img.shields.io/pypi/v/knex)](https://pypi.org/project/knex/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/knex)](https://pypistats.org/packages/knex)

## Installation

`pip install knex`

## Supported Transformers

:x: - Planned

:heavy_check_mark: - Implemented

<!-- markdownlint-disable MD013 -->
<!-- start replace -->
|                                                   General                                                    |                                                       String                                                       |   Number    |          Date           |                                                    Other                                                     |
|--------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------|-------------|-------------------------|--------------------------------------------------------------------------------------------------------------|
|:heavy_check_mark: [Append](https://clay584.github.io/knex/parsers-reference/#knex.parsers.Append)            |:heavy_check_mark: [Base64Decode](https://clay584.github.io/knex/parsers-reference/#knex.parsers.Base64Decode)      |:x: Absolute |:x: BetweenDates         |:x: AsnToInt                                                                                                  |
|:heavy_check_mark: [Count](https://clay584.github.io/knex/parsers-reference/#knex.parsers.Count)              |:heavy_check_mark: [Base64Encode](https://clay584.github.io/knex/parsers-reference/#knex.parsers.Base64Encode)      |:x: Add      |:x: BetweenHours         |:x: DecodeCiscoType7                                                                                          |
|:heavy_check_mark: [FirstElement](https://clay584.github.io/knex/parsers-reference/#knex.parsers.FirstElement)|:heavy_check_mark: [Concat](https://clay584.github.io/knex/parsers-reference/#knex.parsers.Concat)                  |:x: Ceil     |:x: DateStringToISOFormat|:x: EncodeCiscoType7                                                                                          |
|:heavy_check_mark: [GetField](https://clay584.github.io/knex/parsers-reference/#knex.parsers.GetField)        |:x: Cut                                                                                                             |:x: Divide   |:x: DateToEpoch          |:x: EncryptCiscoType5                                                                                         |
|:heavy_check_mark: [GetIndex](https://clay584.github.io/knex/parsers-reference/#knex.parsers.GetIndex)        |:x: DumpJSON                                                                                                        |:x: Floor    |:x: DateToString         |:x: FuzzyWuzzyFind                                                                                            |
|:x: If-Then-Else                                                                                              |:x: FromString                                                                                                      |:x: Modulus  |:x: FormattedDateToEpoch |:x: InterfaceRangeExpand                                                                                      |
|:x: IndexOf                                                                                                   |:x: GenieParse                                                                                                      |:x: Multiply |:x: ModifyDateTime       |:x: IpProtocolNameToNumber                                                                                    |
|:x: Join                                                                                                      |:x: JSONUnescape                                                                                                    |:x: Round    |:x: TimeStampToDate      |:x: IpProtocolNumberToName                                                                                    |
|:x: Jq                                                                                                        |:x: Jinja2Render                                                                                                    |:x: Subtract |                         |:x: JsonSchemaValidate                                                                                        |
|:x: JsonToTable                                                                                               |:heavy_check_mark: [Length](https://clay584.github.io/knex/parsers-reference/#knex.parsers.Length)                  |:x: SumList  |                         |:heavy_check_mark: [MacAddress](https://clay584.github.io/knex/parsers-reference/#knex.parsers.MacAddress)    |
|:heavy_check_mark: [LastElement](https://clay584.github.io/knex/parsers-reference/#knex.parsers.LastElement)  |:x: LoadJSON                                                                                                        |:x: ToPercent|                         |:x: NormalInterfaceName                                                                                       |
|:x: ReverseList                                                                                               |:heavy_check_mark: [RegexExtractAll](https://clay584.github.io/knex/parsers-reference/#knex.parsers.RegexExtractAll)|             |                         |:x: PythonFunction                                                                                            |
|:x: SetIfEmpty                                                                                                |:x: RegexReplace                                                                                                    |             |                         |:x: Random                                                                                                    |
|:x: Slice                                                                                                     |:heavy_check_mark: [Split](https://clay584.github.io/knex/parsers-reference/#knex.parsers.Split)                    |             |                         |:x: SortInterfaceList                                                                                         |
|:x: Sort                                                                                                      |:x: Substring                                                                                                       |             |                         |:heavy_check_mark: [TextFSMParse](https://clay584.github.io/knex/parsers-reference/#knex.parsers.TextFSMParse)|
|:x: Stringify                                                                                                 |:x: TemplateRender                                                                                                  |             |                         |:x: ThisOrThat                                                                                                |
|:x: Unique                                                                                                    |:heavy_check_mark: [ToLower](https://clay584.github.io/knex/parsers-reference/#knex.parsers.ToLower)                |             |                         |:x: ToCamelCase                                                                                               |
|:x: WhereFieldEquals                                                                                          |:x: ToString                                                                                                        |             |                         |:x: ToSnakeCase                                                                                               |
|                                                                                                              |:heavy_check_mark: [ToUpper](https://clay584.github.io/knex/parsers-reference/#knex.parsers.ToUpper)                |             |                         |:x: Ttp                                                                                                       |
|                                                                                                              |:x: Trim                                                                                                            |             |                         |:x: URLDecode                                                                                                 |
|                                                                                                              |:x: YamlDumps                                                                                                       |             |                         |:x: URLEncode                                                                                                 |
|                                                                                                              |:x: YamlLoads                                                                                                       |             |                         |:x: ValidateCiscoType5                                                                                        |
|                                                                                                              |                                                                                                                    |             |                         |:x: ValidateCiscoType7                                                                                        |
|                                                                                                              |                                                                                                                    |             |                         |:x: VlanConfigToList                                                                                          |
|                                                                                                              |                                                                                                                    |             |                         |:x: YamaleValidate                                                                                            |
<!-- end replace -->
<!-- markdownlint-enable MD013 -->

## Usage

```python
>>> from knex.parsers import *
>>>
>>> input_data = """
... Interface             IP-Address      OK?    Method Status          Protocol
... GigabitEthernet0/1    unassigned      YES    unset  up              up
... GigabitEthernet0/2    192.168.190.235 YES    unset  up              up
... GigabitEthernet0/3    unassigned      YES    unset  up              up
... GigabitEthernet0/4    192.168.191.2   YES    unset  up              up
... TenGigabitEthernet2/1 unassigned      YES    unset  up              up
... Virtual36             unassigned      YES    unset  up              up
... """
>>>
>>> pattern = r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"
>>>
>>> end = (
                Start(input_data)
                > RegexExtractAll(pattern)
                > GetIndex(0)
                > Concat("", "/24")
                > IpNetwork()
             )
>>>
>>> print(end.result)
192.168.190.0/24
>>> print(json.dumps(end.history, indent=4))
[
    {
        "parser": "RegexExtractAll",
        "input": "...omitted for brevity...",
        "args": {
            "pattern": "\\b\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\b"
        },
        "error": false,
        "output": [
            "192.168.190.235",
            "192.168.191.2"
        ]
    },
    {
        "parser": "GetIndex",
        "input": [
            "192.168.190.235",
            "192.168.191.2"
        ],
        "args": {
            "idx": 0
        },
        "error": false,
        "output": "192.168.190.235"
    },
    {
        "parser": "Concat",
        "input": "192.168.190.235",
        "args": {
            "prefix": "",
            "suffix": "/24"
        },
        "error": false,
        "output": "192.168.190.235/24"
    },
    {
        "parser": "IpNetwork",
        "input": "192.168.190.235/24",
        "args": {},
        "error": false,
        "output": "192.168.190.0/24"
    }
]
>>>

```

## Development

### Environment Setup

1. Install Poetry
2. Clone the repo: `git clone https://github.com/clay584/knex && cd knex`
3. Install pre-requisits for developement: `poetry install`
4. Activate the environment: `poetry shell`
5. Install git pre-commit hook: `pre-commit install && pre-commit autoupdate`

### Making Changes

1. Run tests and validate coverage: `pytest -v --cov=knex --cov-report html tests`
    * The HTML coverage report will be located at `./htmlcov/index.html`.
2. Commit all changes, and have clean git repo on `main` branch.
3. Bump version: `bump2version <major|minor|patch>`
4. Push to git: `git push && git push --tags`
5. Build for PyPI: Automatically done by Github Actions when a tag is pushed.
6. Publish to PyPI: Automatically done by Github Actions when a tag is pushed.

### Documentation

Docs are created automatically using `mkdocs` and `mkdocstring`.
Testing docs live can be done using `mkdocs serve -a localhost:<port>`.
Docs are built and published automatically using Github Actions.

### Adding a Parser

1. Add the tests for the parser in `./tests/test_knex.py`.
2. Add the parser in `./knex/parsers.py` with docstrings.
3. Write amazing code until all tests are passing.
4. Add the parser in `./knex/__init__.py`.
5. Add the parser in `./gen_table.py`.
6. Run `./gen_table.py`. It will generate that stupid markdown table
and insert it into `README.md`.

### Generating Plain Old requirements.txt

There are a few of the CI tools that require standard requirements.txt format
(not Poetry). Therefore when adding new dependencies with Poetry, we need to
sync those to regular old requirements.txt files. This can be done with the
following commands.

1. `poetry export --without-hashes -f requirements.txt > requirements.txt`
2. `poetry export --without-hashes -f requirements.txt --dev > requirements-dev.txt`

Pre-commit will make sure these are in sync if we forget.
