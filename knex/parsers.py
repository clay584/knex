import base64
from collections import OrderedDict
from ipaddress import IPv4Interface
from typing import List

import regex as re


class KNEXInputMismatch(Exception):
    pass


class Parser:
    history: List = []

    def __init__(self, input=None) -> None:
        self.input = input
        self.result = None

    def process(self):
        return self.input

    def __gt__(self, other):
        # start = self.input
        other.input = self.process()
        other.result = other.process()
        # Append to history, except for the start
        if str(type(self).__name__) != "Start":
            this_history = OrderedDict()
            this_history["parser"] = str(type(self).__name__)
            this_history["input"] = self.input
            this_history["output"] = other.input

            other.history.append(this_history)

        return other.result

    def __str__(self):
        return str(self.process())


class Start(Parser):
    pass


class End(Parser):
    def __str__(self):
        return str(self.result)


class Base64Encode(Parser):
    def process(self) -> str:
        if not isinstance(self.input, str):
            raise KNEXInputMismatch(
                f"{type(self).__name__} KNEX requires input of type 'str'"
            )
        return base64.b64encode(self.input.encode()).decode("ascii")


class Base64Decode(Parser):
    def process(self) -> str:
        if not isinstance(self.input, str):
            raise KNEXInputMismatch(
                f"{type(self).__name__} KNEX requires input of type 'str'"
            )
        return base64.b64decode(self.input).decode()


class Split(Parser):
    def __init__(self, delimeter=" ", **kwargs):
        self.delimeter = delimeter
        super().__init__(**kwargs)

    def process(self) -> List:
        if not isinstance(self.input, str):
            raise KNEXInputMismatch(
                f"{type(self).__name__} KNEX requires input of type 'str'"
            )
        return self.input.split(self.delimeter)


class GetIndex(Parser):
    def __init__(self, idx, **kwargs):
        self.idx = idx
        super().__init__(**kwargs)

    def process(self):
        if not isinstance(self.input, (list, set, tuple)):
            raise KNEXInputMismatch(f"{type(self).__name__} KNEX requires an iterable")
        try:
            return self.input[self.idx]
        except IndexError as e:
            return e


class GetField(Parser):
    def __init__(self, field, **kwargs):
        self.field = field
        super().__init__(**kwargs)

    def process(self):
        if not isinstance(self.input, dict):
            raise KNEXInputMismatch(
                f"{type(self).__name__} KNEX requires an input of dictionary"
            )
        try:
            return self.input[self.field]
        except Exception as e:
            return e


class Count(Parser):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def process(self):
        return len(self.input)


class ToLower(Parser):
    def process(self) -> str:
        if not isinstance(self.input, str):
            raise KNEXInputMismatch(
                f"{type(self).__name__} KNEX requires input of type 'str'"
            )
        return self.input.lower()


class ToUpper(Parser):
    def process(self) -> str:
        if not isinstance(self.input, str):
            raise KNEXInputMismatch(
                f"{type(self).__name__} KNEX requires input of type 'str'"
            )
        return self.input.upper()


class IpNetwork(Parser):
    def process(self) -> str:
        if not isinstance(self.input, str):
            raise KNEXInputMismatch(
                f"{type(self).__name__} KNEX requires input of type 'str'"
            )
        return str(IPv4Interface(self.input).network)


class RegexExtractAll(Parser):
    def __init__(self, pattern, **kwargs):
        self.pattern = pattern
        super().__init__(**kwargs)

    def process(self) -> str:
        if not isinstance(self.input, str):
            raise KNEXInputMismatch(
                f"{type(self).__name__} KNEX requires input of type 'str'"
            )
        return re.findall(self.pattern, self.input)


class Concat(Parser):
    def __init__(self, prefix="", suffix="", **kwargs):
        self.prefix = prefix
        self.suffix = suffix
        super().__init__(**kwargs)

    def process(self):
        if not isinstance(self.input, str):
            raise KNEXInputMismatch(
                f"{type(self).__name__} KNEX requires an input of type 'str'"
            )
        return self.prefix + self.input + self.suffix


class Append(Parser):
    def __init__(self, suffix="", **kwargs):
        self.suffix = suffix
        super().__init__(**kwargs)

    def process(self):
        if not isinstance(self.input, str):
            raise KNEXInputMismatch(
                f"{type(self).__name__} KNEX requires an input of type 'str'"
            )
        return self.input + self.suffix
