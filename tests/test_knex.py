from knex import __version__
from knex.parsers import (
    Append,
    Base64Decode,
    Base64Encode,
    Concat,
    Count,
    End,
    GetField,
    GetIndex,
    IpNetwork,
    Parser,
    RegexExtractAll,
    Split,
    Start,
    ToLower,
    ToUpper,
)


def test_version():
    assert __version__ == "0.1.2"  # nosec B101


def test_start():
    assert str(Parser("clay,michelle")) == "clay,michelle"  # nosec B101


def test_end():
    assert End().result is None  # nosec B101


def test_b64_encode():
    start = Parser("clay,michelle")
    end = End()
    start > Base64Encode() > end
    assert end.result == "Y2xheSxtaWNoZWxsZQ=="  # nosec B101


def test_b64_decode():
    start = Parser("Y2xheSxtaWNoZWxsZQ==")
    end = End()
    start > Base64Decode() > end
    assert end.result == "clay,michelle"  # nosec B101


def test_split():
    start = Parser("clay,michelle")
    end = End()
    start > Split(",") > end
    assert end.result == ["clay", "michelle"]  # nosec B101


def test_get_index():
    start = Parser(["clay", "michelle"])
    end = End()
    start > GetIndex(1) > end
    assert end.result == "michelle"  # nosec B101


def test_get_field():
    start = Parser({"foo": "bar", "buzz": "baz"})
    end = End()
    start > GetField("foo") > end
    assert end.result == "bar"  # nosec B101


def test_count():
    start = Parser({"foo": "bar", "buzz": "baz"})
    end = End()
    start > Count() > end
    assert end.result == 2  # nosec B101


def test_to_lower():
    start = Parser("FOOBAR")
    end = End()
    start > ToLower() > end
    assert end.result == "foobar"  # nosec B101


def test_to_upper():
    start = Parser("foobar")
    end = End()
    start > ToUpper() > end
    assert end.result == "FOOBAR"  # nosec B101


def test_ip_network():
    start = Parser("192.168.1.55/24")
    end = End()
    start > IpNetwork() > end
    assert end.result == "192.168.1.0/24"  # nosec B101


def test_regex_extract():
    output = """
Interface             IP-Address      OK?    Method Status     	Protocol
GigabitEthernet0/1    unassigned      YES    unset  up         	up
GigabitEthernet0/2    192.168.190.235 YES    unset  up         	up
GigabitEthernet0/3    unassigned      YES    unset  up         	up
GigabitEthernet0/4    192.168.191.2   YES    unset  up         	up
TenGigabitEthernet2/1 unassigned      YES    unset  up         	up
TenGigabitEthernet2/2 unassigned      YES    unset  up         	up
TenGigabitEthernet2/3 unassigned      YES    unset  up         	up
TenGigabitEthernet2/4 unassigned      YES    unset  down       	down
GigabitEthernet36/1   unassigned      YES    unset  down        down
GigabitEthernet36/2   unassigned      YES    unset  down        down
GigabitEthernet36/11  unassigned      YES    unset  down       	down
GigabitEthernet36/25  unassigned      YES    unset  down       	down
Te36/45               unassigned      YES    unset  down       	down
Te36/46               unassigned      YES    unset  down       	down
Te36/47               unassigned      YES    unset  down       	down
Te36/48               unassigned      YES    unset  down       	down
Virtual36             unassigned      YES    unset  up         	up
"""
    start = Parser(output)
    end = End()
    pattern = r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"
    start > RegexExtractAll(pattern) > end
    assert end.result == [  # nosec B101
        "192.168.190.235",
        "192.168.191.2",
    ]


def test_chain1():
    start = Parser("clay,michelle")
    end = End()
    start > Base64Encode() > Base64Decode() > Split(",") > GetIndex(0) > end
    assert end.result == "clay"  # nosec B101


def test_concat():
    start = Start("baz")
    end = End()
    start > Concat("foo", "bar") > end

    assert end.result == "foobazbar"  # nosec B101


def test_append():
    start = Start("foo")
    end = End()
    start > Append("bar") > end

    assert end.result == "foobar"  # nosec B101
