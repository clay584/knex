from knex import __version__
from knex.parsers import (
    Base64Decode,
    Base64Encode,
    Count,
    GetField,
    GetIndex,
    IpNetwork,
    Parser,
    RegexExtractAll,
    Split,
    ToLower,
    ToUpper,
)


def test_version():
    assert __version__ == "0.1.2"  # nosec B101


def test_starter():
    assert str(Parser("clay,michelle")) == "clay,michelle"  # nosec B101


def test_b64_encode():
    starter = Parser("clay,michelle")
    assert (starter > Base64Encode()) == "Y2xheSxtaWNoZWxsZQ=="  # nosec B101


def test_b64_decode():
    starter = Parser("Y2xheSxtaWNoZWxsZQ==")
    assert (starter > Base64Decode()) == "clay,michelle"  # nosec B101


def test_split():
    starter = Parser("clay,michelle")
    assert (starter > Split(delimeter=",")) == ["clay", "michelle"]  # nosec B101


def test_get_index():
    starter = Parser(["clay", "michelle"])
    assert (starter > GetIndex(1)) == "michelle"  # nosec B101


def test_get_field():
    starter = Parser({"foo": "bar", "buzz": "baz"})
    assert (starter > GetField("foo")) == "bar"  # nosec B101


def test_count():
    starter = Parser({"foo": "bar", "buzz": "baz"})
    assert (starter > Count()) == 2  # nosec B101


def test_to_lower():
    starter = Parser("FOOBAR")
    assert (starter > ToLower()) == "foobar"  # nosec B101


def test_to_upper():
    starter = Parser("foobar")
    assert (starter > ToUpper()) == "FOOBAR"  # nosec B101


def test_ip_network():
    starter = Parser("192.168.1.55/24")
    assert (starter > IpNetwork()) == "192.168.1.0/24"  # nosec B101


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
    starter = Parser(output)

    pattern = r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"

    assert (starter > RegexExtractAll(pattern)) == ["192.168.190.235", "192.168.191.2"]


def test_chain1():
    starter = Parser("clay,michelle")
    assert (  # nosec B101
        starter
        > Base64Encode()
        > Base64Decode()
        > Split(delimeter=",")
        > GetIndex(idx=0)
    ) == "clay"
