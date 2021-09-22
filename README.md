# KNEX

Python library for creating chainable data transformers.

## Installation

`pip install knex`

## Supported Transformers

:x: - Planned

:heavy_check_mark: - Implemented

<!-- markdownlint-disable MD013 -->
| General                           | String                               | Number        | Date                      | Other          |
| --------------------------------- | ------------------------------------ | ------------- | ------------------------- | -------------- |
| :heavy_check_mark: Append       | :heavy_check_mark: Base64Decode    | :x: Absolute  | :x: BetweenDates          | :heavy_check_mark: TextFSMParse |
| :heavy_check_mark: Count        | :heavy_check_mark: Base64Encode    | :x: Add       | :x: BetweenHours          | :x: ThisOrThat  |
| :heavy_check_mark: FirstElement | :heavy_check_mark: Concat          | :x: Ceil      | :x: DateStringToISOFormat | :x: Ttp  |
| :heavy_check_mark: GetField     | :x: Cut                              | :x: Divide    | :x: DateToEpoch           |       :x: URLDecode         |
| :heavy_check_mark: GetIndex     | :x: DumpJSON                         | :x: Floor     | :x: DateToString          |         :x: URLEncode       |
| :x: If-Then-Else                  | :x: FromString                       | :x: Modulus   | :x: FormattedDateToEpoch  |
| :x: IndexOf                       | :x: JSONUnescape                     | :x: Multiply  | :x: ModifyDateTime        |                |
| :x: Join                          | :heavy_check_mark: Length          | :x: Round     | :x: TimeStampToDate       |                |
| :x: Jq                            | :x: LoadJSON                         | :x: Subtract  |                           |                |
| :x: JsonToTable                   | :heavy_check_mark: RegexExtractAll | :x: SumList   |                           |                |
| :heavy_check_mark: LastElement  | :x: RegexReplace                     | :x: ToPercent |                           |
| :x: ReverseList                   | :heavy_check_mark: Split           |               |                           |                |
| :x: SetIfEmpty                    | :x: Substring                        |               |                           |                |
| :x: Slice                         | :heavy_check_mark: ToLower         |               |                           |                |
| :x: Sort                          | :x: ToString                         |               |                           |                |
| :x: Stringify                     | :heavy_check_mark: ToUpper         |               |                           |                |
| :x: Unique                        | :x: Trim                             |               |                           |                |
| :x: WhereFieldEquals              |                                      |               |                           |                |
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
2. Commit all changes, and have clean git repo on `main` branch.
3. Bump version: `bump2version <major|minor|patch>`
4. Push to git: `git push && git push --tags`
5. Build for PyPI: Automatically done by Github Actions when a tag is pushed.
6. Publish to PyPI: Automatically done by Github Actions when a tag is pushed.
