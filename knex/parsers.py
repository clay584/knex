import base64
from collections import OrderedDict
from copy import copy
from ipaddress import IPv4Interface
import textfsm
import tempfile
import regex as re


class Parser:
    def __init__(self, input=None, raise_exception=False, *args, **kwargs):
        self.input = input
        self.raise_exception = raise_exception
        self.result = None
        self.args = None
        self.error = False
        super().__init__(*args, **kwargs)

    def process(self):
        return self.input

    def get_args(self):
        args = copy(self.__dict__)
        args.pop("input")
        args.pop("result")
        args.pop("args")
        args.pop("error")
        args.pop("raise_exception")
        try:
            args.pop("history")
        except KeyError:
            pass
        return args

    def __gt__(self, other):
        other.raise_exception = self.raise_exception
        other.input = self.process()
        other.result = other.process()
        history = OrderedDict()
        history["parser"] = str(type(other).__name__)
        history["input"] = other.input
        history["args"] = other.get_args()
        history["error"] = other.error
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


class Base64Encode(Parser):
    def process(self):
        if self.raise_exception:
            return base64.b64encode(self.input.encode()).decode("ascii")
        try:
            return base64.b64encode(self.input.encode()).decode("ascii")
        except Exception as e:
            self.error = True
            return str(e)


class Base64Decode(Parser):
    def process(self):
        if self.raise_exception:
            return base64.b64decode(self.input).decode()
        try:
            return base64.b64decode(self.input).decode()
        except Exception as e:
            self.error = True
            return str(e)


class Split(Parser):
    def __init__(self, delimeter=" ", *args, **kwargs):
        self.delimeter = delimeter
        super().__init__(*args, **kwargs)
        # self.args = self.get_args()

    def process(self):
        if self.raise_exception:
            return self.input.split(self.delimeter)
        try:
            return self.input.split(self.delimeter)
        except Exception as e:
            self.error = True
            return str(e)


class GetIndex(Parser):
    def __init__(self, idx, *args, **kwargs):
        self.idx = idx
        super().__init__(*args, **kwargs)
        # self.args = self.get_args()

    def process(self):
        if self.raise_exception:
            return self.input[self.idx]
        try:
            return self.input[self.idx]
        except Exception as e:
            self.error = True
            return str(e)


class ToUpper(Parser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def process(self):
        if self.raise_exception:
            return self.input.upper()
        try:
            return self.input.upper()
        except Exception as e:
            self.error = True
            return str(e)


class GetField(Parser):
    def __init__(self, field, *args, **kwargs):
        self.field = field
        super().__init__(*args, **kwargs)

    def process(self):
        if self.raise_exception:
            return self.input[self.field]
        try:
            return self.input[self.field]
        except Exception as e:
            self.error = True
            return str(e)


class Count(Parser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def process(self):
        if self.raise_exception:
            return len(self.input)
        try:
            return len(self.input)
        except Exception as e:
            self.error = True
            return str(e)


class ToLower(Parser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def process(self):
        if self.raise_exception:
            return self.input.lower()
        try:
            return self.input.lower()
        except Exception as e:
            self.error = True
            return str(e)


class IpNetwork(Parser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def process(self):
        if self.raise_exception:
            return str(IPv4Interface(self.input).network)
        try:
            return str(IPv4Interface(self.input).network)
        except Exception as e:
            self.error = True
            return str(e)


class RegexExtractAll(Parser):
    def __init__(self, pattern, *args, **kwargs):
        self.pattern = pattern
        super().__init__(*args, **kwargs)

    def process(self):
        if self.raise_exception:
            return re.findall(self.pattern, self.input)
        try:
            return re.findall(self.pattern, self.input)
        except Exception as e:
            self.error = True
            return str(e)


class Concat(Parser):
    def __init__(self, prefix="", suffix="", *args, **kwargs):
        self.prefix = prefix
        self.suffix = suffix
        super().__init__(*args, **kwargs)

    def process(self):
        if self.raise_exception:
            return self.prefix + self.input + self.suffix
        try:
            return self.prefix + self.input + self.suffix
        except Exception as e:
            self.error = True
            return str(e)


class Append(Parser):
    def __init__(self, suffix="", *args, **kwargs):
        self.suffix = suffix
        super().__init__(*args, **kwargs)

    def process(self):
        if self.raise_exception:
            return self.input + self.suffix
        try:
            return self.input + self.suffix
        except Exception as e:
            self.error = True
            return str(e)


class FirstElement(Parser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def process(self):
        if self.raise_exception:
            return self.input[0]
        try:
            return self.input[0]
        except Exception as e:
            self.error = True
            return str(e)


class LastElement(Parser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def process(self):
        if self.raise_exception:
            return self.input[-1]
        try:
            return self.input[-1]
        except Exception as e:
            self.error = True
            return str(e)


class TextFSMParse(Parser):
    def __init__(self, template, fmt="dict", *args, **kwargs):
        self.template = template
        self.fmt = fmt if fmt == "dict" else "default"
        super().__init__(*args, **kwargs)

    def _to_dict(self, data, headers):
        results = []
        for i in data:
            this_dict = {headers[count].lower(): j for count, j in enumerate(i)}
            results.append(this_dict)
        return {"result": results}

    def process(self):
        if self.raise_exception:
            with tempfile.NamedTemporaryFile() as fakefile:
                fakefile.write(self.template.encode("utf-8"))
                fakefile.seek(0)
                parser = textfsm.TextFSM(fakefile)
                parsed = parser.ParseText(self.input)
                headers = parser.header
            if self.fmt == "dict":
                return self._to_dict(parsed, headers)
            return parsed
        try:
            with tempfile.NamedTemporaryFile() as fakefile:
                fakefile.write(self.template.encode("utf-8"))
                fakefile.seek(0)
                parser = textfsm.TextFSM(fakefile)
                parsed = parser.ParseText(self.input)
                headers = parser.header
            if self.fmt == "dict":
                return self._to_dict(parsed, headers)
            return parsed
        except Exception as e:
            self.error = True
            return str(e)
