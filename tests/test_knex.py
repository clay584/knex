from knex import __version__
from knex.parsers import (
    Append,
    Base64Decode,
    Base64Encode,
    Concat,
    Count,
    FirstListElement,
    GetField,
    GetIndex,
    IpNetwork,
    LastListElement,
    Parser,
    RegexExtractAll,
    Split,
    Start,
    ToLower,
    ToUpper,
)


def test_version():
    assert __version__ == "0.1.2"  # nosec B101


def test_parser():
    assert str(Parser("clay,michelle")) == "clay,michelle"  # nosec B101


def test_start():
    assert Start("foobar").result == "foobar"  # nosec B101


def test_b64_encode():
    assert (  # nosec B101
        Start("clay,michelle") > Base64Encode()
    ).result == "Y2xheSxtaWNoZWxsZQ=="


def test_b64_decode():
    assert (  # nosec B101
        Start("Y2xheSxtaWNoZWxsZQ==") > Base64Decode()
    ).result == "clay,michelle"


def test_split():
    assert (Start("clay,michelle") > Split(",")).result == [  # nosec B101
        "clay",
        "michelle",
    ]


def test_get_index():
    assert (  # nosec B101
        Start(["clay", "michelle"]) > GetIndex(1)
    ).result == "michelle"


def test_get_field():
    assert (  # nosec B101
        Start({"foo": "bar", "buzz": "baz"}) > GetField("foo")
    ).result == "bar"


def test_count():
    assert (Start({"foo": "bar", "buzz": "baz"}) > Count()).result == 2  # nosec B101


def test_to_lower():
    assert (Start("FOOBAR") > ToLower()).result == "foobar"  # nosec B101


def test_to_upper():
    assert (Start("foobar") > ToUpper()).result == "FOOBAR"  # nosec B101


def test_ip_network():
    assert (  # nosec B101
        Start("192.168.1.55/24") > IpNetwork()
    ).result == "192.168.1.0/24"


def test_regex_extract():
    rtr_output = """
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

    pattern = r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"
    assert (Start(rtr_output) > RegexExtractAll(pattern)).result == [  # nosec B101
        "192.168.190.235",
        "192.168.191.2",
    ]


def test_chain1():
    assert (  # nosec B101
        Start("clay,michelle")
        > Base64Encode()
        > Base64Decode()
        > Split(",")
        > GetIndex(0)
        > ToUpper()
    ).result == "CLAY"


def test_concat():
    assert (Start("baz") > Concat("foo", "bar")).result == "foobazbar"  # nosec B101


def test_append():
    assert (Start("foo") > Append("bar")).result == "foobar"  # nosec B101


def test_first_list_element():
    assert (Start(["foo", "bar"]) > FirstListElement()).result == "foo"  # nosec B101


def test_last_list_element():
    assert (Start(["foo", "bar"]) > LastListElement()).result == "bar"  # nosec B101
