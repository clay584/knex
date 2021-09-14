import base64
from collections import OrderedDict
from copy import copy
from ipaddress import IPv4Interface
from typing import List

import regex as re


class KNEXInputMismatch(Exception):
    pass


class Parser:
    def __init__(self, input=None, *args, **kwargs):
        self.input = input
        self.result = None
        # self.history: List = []
        self.args = None
        super().__init__(*args, **kwargs)

    def process(self):
        return self.input

    def get_args(self):
        args = copy(self.__dict__)
        args.pop("input")
        args.pop("result")
        args.pop("args")
        try:
            args.pop("history")
        except Exception:
            pass
        return args

    # def gen_history(self):
    #     this_history = OrderedDict()
    #     this_history["input"] = other.input
    #     this_history["parser"] = str(type(other).__name__)
    #     this_history["args"] = other.get_args()
    #     this_history["reuslt"] = other.result
    #     return this_history

    def __gt__(self, other):
        # start = self.input
        other.input = self.process()
        other.result = other.process()
        # Append to history, except for the start
        # if str(type(self).__name__) != "Start":
        history = OrderedDict()
        history["input"] = other.input
        history["parser"] = str(type(other).__name__)
        history["args"] = other.get_args()
        history["output"] = other.result

        if hasattr(self, "history") and self.history is not None:
            other.history = copy(self.history)
            other.history.append(history)
        else:
            other.history = [history]

        return other

    def __str__(self):
        return str(self.process())


class Start(Parser):
    def __init__(self, input, *args, **kwargs):
        super().__init__(input, *args, **kwargs)
        self.result = self.input
        self.args = self.get_args()

    # def __init__(self, input):
    # super().__init__(input)


class End(Parser):
    def __str__(self):
        return str(self.result)


class Base64Encode(Parser):
    def process(self):
        if not isinstance(self.input, str):
            raise KNEXInputMismatch(
                f"{type(self).__name__} KNEX requires input of type 'str'"
            )
        return base64.b64encode(self.input.encode()).decode("ascii")


class Base64Decode(Parser):
    def process(self):
        if not isinstance(self.input, str):
            raise KNEXInputMismatch(
                f"{type(self).__name__} KNEX requires input of type 'str'"
            )
        return base64.b64decode(self.input).decode()


class Split(Parser):
    def __init__(self, delimeter=" ", *args, **kwargs):
        self.delimeter = delimeter
        super().__init__(*args, **kwargs)
        self.args = self.get_args()

    def process(self):
        if not isinstance(self.input, str):
            raise KNEXInputMismatch(
                f"{type(self).__name__} KNEX requires input of type 'str'"
            )
        return self.input.split(self.delimeter)


class GetIndex(Parser):
    def __init__(self, idx, *args, **kwargs):
        self.idx = idx
        super().__init__(*args, **kwargs)
        self.args = self.get_args()

    def process(self):
        if not isinstance(self.input, (list, set, tuple)):
            raise KNEXInputMismatch(f"{type(self).__name__} KNEX requires an iterable")
        try:
            return self.input[self.idx]
        except IndexError as e:
            return e


class ToUpper(Parser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def process(self):
        if not isinstance(self.input, str):
            raise KNEXInputMismatch(
                f"{type(self).__name__} KNEX requires input of type 'str'"
            )
        return self.input.upper()


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
    def process(self):
        if not isinstance(self.input, str):
            raise KNEXInputMismatch(
                f"{type(self).__name__} KNEX requires input of type 'str'"
            )
        return self.input.lower()


class IpNetwork(Parser):
    def process(self):
        if not isinstance(self.input, str):
            raise KNEXInputMismatch(
                f"{type(self).__name__} KNEX requires input of type 'str'"
            )
        return str(IPv4Interface(self.input).network)


class RegexExtractAll(Parser):
    def __init__(self, pattern, **kwargs):
        self.pattern = pattern
        super().__init__(**kwargs)

    def process(self):
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


class FirstListElement(Parser):
    def process(self):
        if not isinstance(self.input, (list, set, tuple)):
            raise KNEXInputMismatch(
                f"{type(self).__name__} KNEX requires input of iterable"
            )
        return self.input[0]


class LastListElement(Parser):
    def process(self):
        if not isinstance(self.input, (list, set, tuple)):
            raise KNEXInputMismatch(
                f"{type(self).__name__} KNEX requires input of iterable"
            )
        return self.input[-1]
