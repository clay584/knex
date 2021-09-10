from knex import __version__
from knex.parsers import (
    Base64Decode,
    Base64Encode,
    Count,
    GetField,
    GetIndex,
    Parser,
    Split,
    ToLower,
    ToUpper,
)


def test_version():
    assert __version__ == "0.1.2"  # nosec B101


def test_starter():
    assert str(Parser("clay,michelle")) == "clay,michelle"


def test_b64_encode():
    starter = Parser("clay,michelle")
    assert (starter > Base64Encode()) == "Y2xheSxtaWNoZWxsZQ=="


def test_b64_decode():
    starter = Parser("Y2xheSxtaWNoZWxsZQ==")
    assert (starter > Base64Decode()) == "clay,michelle"


def test_split():
    starter = Parser("clay,michelle")
    assert (starter > Split(delimeter=",")) == ["clay", "michelle"]


def test_get_index():
    starter = Parser(["clay", "michelle"])
    assert (starter > GetIndex(1)) == "michelle"


def test_get_field():
    starter = Parser({"foo": "bar", "buzz": "baz"})
    assert (starter > GetField("foo")) == "bar"


def test_count():
    starter = Parser({"foo": "bar", "buzz": "baz"})
    assert (starter > Count()) == 2


def test_to_lower():
    starter = Parser("FOOBAR")
    assert (starter > ToLower()) == "foobar"


def test_to_upper():
    starter = Parser("foobar")
    assert (starter > ToUpper()) == "FOOBAR"


def test_chain1():
    starter = Parser("clay,michelle")
    assert (
        starter
        > Base64Encode()
        > Base64Decode()
        > Split(delimeter=",")
        > GetIndex(idx=0)
    ) == "clay"
