# KNEX

Python library for creating chainable data transformers.

## Installation

`pip install knex`

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
