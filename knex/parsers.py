import base64
from typing import Any, Dict, List, Union


class KNEXInputMismatch(Exception):
    pass


class Parser:
    def __init__(self, input=None) -> None:
        self.input = input

    def process(self):
        return self.input

    def __gt__(self, other):
        other.input = self.process()
        return other.process()

    def __str__(self):
        return str(self.process())


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
