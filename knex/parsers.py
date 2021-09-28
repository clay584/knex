import base64
from collections import OrderedDict
from copy import copy
from ipaddress import IPv4Interface
import textfsm
import tempfile
import regex as re
from macaddr import MacAddress as MacAddr


class Parser:

    """Base Parser object"""

    def __init__(self, input_data=None, raise_exception=False, *args, **kwargs):
        """Base parser initialization. This does not need to be called as an end user of this library.
        Args:
            input_data (Any, optional): Input to the parser. Defaults to None.
            raise_exception (bool, optional): Whether or not to raise a proper python exception if there is a parsing failure. Defaults to False.

        """
        self.input = input_data
        self.raise_exception = raise_exception
        self.result = None
        self.args = None
        self.error = False
        super().__init__(*args, **kwargs)

    def process(self):
        """Process method. Takes input, and trasforms it.

        Returns:
            Any: Output from the transformation.
        """
        return self.input

    def get_args(self):
        """Get arguments passed into the parser

        Returns:
            dict: All arguments passed in, and their values.
        """
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
        """Greater-than `>` dunder method overload allowing for the chaining of parsers together. (e.g. `Parser > Parser > Parser`)

        Args:
            other (Parser): The right hand operand being fed into the `__gt__` method. (`LeftHandOperand > RightHandOperand`)

        Returns:
            other: Returns the right hand operand after processing is completed.
        """
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
    """Starting parser object. All transformations must start with the Start object."""

    def __init__(self, input_data, *args, **kwargs):
        """Starter object to begin a chain of parsing.

        Args:
            input (Any): Any form of input that is to be parsed so long as it is a simple data type. (e.g. numbers, sequences, dicts, sets, etc.)
        """
        super().__init__(input_data, *args, **kwargs)
        self.result = self.input
        self.args = self.get_args()


class Base64Encode(Parser):
    """Base64 encode a string"""

    def process(self):
        """Process a string and return its base64 encoded value.

        Returns:
            str: Base64 encoded string in ascii
        """
        if self.raise_exception:
            return base64.b64encode(self.input.encode()).decode("ascii")
        try:
            return base64.b64encode(self.input.encode()).decode("ascii")
        except Exception as e:
            self.error = True
            return str(e)


class Base64Decode(Parser):
    """Base64 decode a string"""

    def process(self):
        """Process a base64 encoded string, and return its decoded value.

        Returns:
            [type]: [description]
        """
        if self.raise_exception:
            return base64.b64decode(self.input).decode()
        try:
            return base64.b64decode(self.input).decode()
        except Exception as e:
            self.error = True
            return str(e)


class Split(Parser):
    """Split a string into a list"""

    def __init__(self, delimeter=" ", *args, **kwargs):
        """Initialize Split class

        Args:
            delimeter (str, optional): Delimiter for which to split string with. Defaults to " ".
        """
        self.delimeter = delimeter
        super().__init__(*args, **kwargs)
        # self.args = self.get_args()

    def process(self):
        """Splits string into its parts.

        Returns:
            list: A list of parts of the original input.
        """
        if self.raise_exception:
            return self.input.split(self.delimeter)
        try:
            return self.input.split(self.delimeter)
        except Exception as e:
            self.error = True
            return str(e)


class GetIndex(Parser):
    """Gets an element of an iterable like a list or set"""

    def __init__(self, idx, *args, **kwargs):
        """Initialize by providing the index of the element to return.

        Args:
            idx (int): Index of the element to fetch from the iterable
        """
        self.idx = idx
        super().__init__(*args, **kwargs)
        # self.args = self.get_args()

    def process(self):
        """Fetches the value of the index of the iterable given in as input.

        Returns:
            Any: The value contained in the iterable at the provided index.
        """
        if self.raise_exception:
            return self.input[self.idx]
        try:
            return self.input[self.idx]
        except Exception as e:
            self.error = True
            return str(e)


class ToUpper(Parser):
    """Convert string to upper case"""

    def process(self):
        """Process an input string and convert to upper case.

        Returns:
            str: Upper cased string.
        """
        if self.raise_exception:
            return self.input.upper()
        try:
            return self.input.upper()
        except Exception as e:
            self.error = True
            return str(e)


class GetField(Parser):
    """Get the value of a dictionary by key"""

    def __init__(self, field, *args, **kwargs):
        """Initialize GetField class.

        Args:
            field (str): The key name to fetch.
        """
        self.field = field
        super().__init__(*args, **kwargs)

    def process(self):
        """Fetches the value in a dict given the provided key.

        Returns:
            Any: The value of the provided key in the input dictionary.
        """
        if self.raise_exception:
            return self.input[self.field]
        try:
            return self.input[self.field]
        except Exception as e:
            self.error = True
            return str(e)


class Count(Parser):
    """Count the number of items in an iterable"""

    def process(self):
        """Counts the number of items in an iterable.

        Returns:
            int: The number of items found.
        """
        if self.raise_exception:
            return len(self.input)
        try:
            return len(self.input)
        except Exception as e:
            self.error = True
            return str(e)


class ToLower(Parser):
    """Convert a string to lower case"""

    def process(self):
        """Convert string to lower case.

        Returns:
            str: Lower cased string.
        """
        if self.raise_exception:
            return self.input.lower()
        try:
            return self.input.lower()
        except Exception as e:
            self.error = True
            return str(e)


class IpNetwork(Parser):
    """Calculates the Network Address of a given IP address in CIDR notation"""

    def process(self):
        """Calculate network address and prefix given a CIDR notated IPv4 address.

        Returns:
            str: Network address and prefix length in CIDR notation (e.g. 10.0.0.0/24)
        """
        if self.raise_exception:
            return str(IPv4Interface(self.input).network)
        try:
            return str(IPv4Interface(self.input).network)
        except Exception as e:
            self.error = True
            return str(e)


class RegexExtractAll(Parser):
    """Extract all matches from a string given a regex pattern"""

    def __init__(self, pattern, *args, **kwargs):
        """Extract all matches from a string given a regex pattern

        Args:
            pattern (str): Regular expression pattern (not compiled)
        """
        self.pattern = pattern
        super().__init__(*args, **kwargs)

    def process(self):
        """Process string with regex pattern and return matches or None.

        Returns:
            list, None: A list of matches or None if no matches found.
        """
        if self.raise_exception:
            return re.findall(self.pattern, self.input)
        try:
            return re.findall(self.pattern, self.input)
        except Exception as e:
            self.error = True
            return str(e)


class Concat(Parser):
    """Concatinate string with optional prefix and suffix"""

    def __init__(self, prefix="", suffix="", *args, **kwargs):
        """Initialize Concat class.

        Args:
            prefix (str, optional): Prefix to append to front of input. Defaults to "".
            suffix (str, optional): Suffix to append to end of input. Defaults to "".
        """
        self.prefix = prefix
        self.suffix = suffix
        super().__init__(*args, **kwargs)

    def process(self):
        """Process input string and concatinate with prefix and suffix.

        Returns:
            str: Concatinated string.
        """
        if self.raise_exception:
            return self.prefix + self.input + self.suffix
        try:
            return self.prefix + self.input + self.suffix
        except Exception as e:
            self.error = True
            return str(e)


class Append(Parser):
    """Append value to end of string"""

    def __init__(self, suffix="", *args, **kwargs):
        """Initialize Append class.

        Args:
            suffix (str, optional): Suffix to append to end of string. Defaults to "".
        """
        self.suffix = suffix
        super().__init__(*args, **kwargs)

    def process(self):
        """Append input with suffix.

        Returns:
            str: Appended string.
        """
        if self.raise_exception:
            return self.input + self.suffix
        try:
            return self.input + self.suffix
        except Exception as e:
            self.error = True
            return str(e)


class FirstElement(Parser):
    """Get first element of iterable"""

    def process(self):
        """Get first element of input iterable.

        Returns:
            Any: The first element of the input iterable.
        """
        if self.raise_exception:
            return self.input[0]
        try:
            return self.input[0]
        except Exception as e:
            self.error = True
            return str(e)


class LastElement(Parser):
    """Get last element of iterable"""

    def process(self):
        """Get last element of the input iterable.

        Returns:
            Any: The last element of the input iterable.
        """
        if self.raise_exception:
            return self.input[-1]
        try:
            return self.input[-1]
        except Exception as e:
            self.error = True
            return str(e)


class TextFSMParse(Parser):
    """Parse text using TextFSM parser"""

    def __init__(self, template, *args, fmt="dict", **kwargs):
        """Initialize class by providing a template as a string.

        Args:
            template (str): TextFSM template string (not a file handle object as TextFSM usually requires)
            fmt (str, optional): Output format. `dict` format will return a list of dicts, \
            but `native` format will return the native TextFSM format. Options are `dict` or `native`. Defaults to `dict`.
        """
        self.template = template
        self.fmt = fmt if fmt == "dict" else "native"
        super().__init__(*args, **kwargs)

    @staticmethod
    def _to_dict(data, headers):
        """Utility method to convert native TextFSM format to list of dicts.

        Args:
            data (Any): Native TextFSM parsed object.
            headers (list): List of field names (equivalent of headers of a CSV file).

        Returns:
            list: Returns list of dicts of TextFSM parsed data.
        """
        results = []
        for i in data:
            this_dict = {headers[count].lower(): j for count, j in enumerate(i)}
            results.append(this_dict)
        return {"result": results}

    def _parse(self):
        """Parse with TextFSM library.

        Returns:
            list: List of results from TextFSM parsing in native TextFSM format.
        """
        with tempfile.NamedTemporaryFile() as fakefile:
            fakefile.write(self.template.encode("utf-8"))
            fakefile.seek(0)
            parser = textfsm.TextFSM(fakefile)
            parsed = parser.ParseText(self.input)
            headers = parser.header
        if self.fmt == "dict":
            return self._to_dict(parsed, headers)
        return parsed

    def process(self):
        """Parse text with TextFSM parser.

        Returns:
            list: Native TextFSM parsed data in `dict` or `native` format.
        """
        if self.raise_exception:
            return self._parse()
        try:
            return self._parse()
        except Exception as e:
            self.error = True
            return str(e)


class MacAddress(Parser):
    """Parse MAC addresses and output in user-defined format"""

    def __init__(self, *args, size=2, sep=":", **kwargs):
        """Initialize by providing size and separator.

        Args:
            size (int, optional): Group size between separators. Defaults to 2.
            sep (str, optional): Separator between octets of the mac address. Defaults to ":".
        """
        self.size = size
        self.sep = sep
        super().__init__(*args, **kwargs)

    def process(self):
        """Parse and format mac address.

        Returns:
            str: Mac address in user provided format.
        """
        if self.raise_exception:
            mac = MacAddr(self.input)
            return mac.format(size=self.size, sep=self.sep)
        try:
            mac = MacAddr(self.input)
            return mac.format(size=self.size, sep=self.sep)
        except Exception as e:
            self.error = True
            return str(e)
