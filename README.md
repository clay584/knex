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
>>> result = (
                Start(input_data)
                > RegexExtractAll(pattern)
                > GetIndex(0)
                > Concat("", "/24")
                > IpNetwork()
             ).result
>>>
>>> print(result)
192.168.190.0/24
>>>

```

## Development

### Environment Setup

1. Install Poetry
2. Clone the repo: `git clone https://github.com/clay584/knex && cd knex`
3. Install pre-requisits for developement: `poetry install`
4. Install PyPI API Key: `poetry config pypi-token.pypi <token>`
5. Activate the environment: `poetry shell`
6. Install git pre-commit hook: `pre-commit install && pre-commit autoupdate`

### Publishing to PyPI

1. Run tests and validate coverage: `pytest -v --cov=knex --cov-report html tests`
2. Commit all changes, and have clean git repo on `main` branch.
3. Bump version: `bump2version <major|minor|patch>`
4. Push to git: `git push origin main --tags`
5. Build for PyPI: `poetry build`
6. Publish to PyPI: `poetry publish`
