import json
import os
from knex import __version__
from knex.parsers import (
    Append,
    Base64Decode,
    Base64Encode,
    Concat,
    Count,
    FirstElement,
    GetField,
    GetIndex,
    IpNetwork,
    LastElement,
    Parser,
    RegexExtractAll,
    Split,
    Start,
    ToLower,
    ToUpper,
    TextFSMParse,
    MacAddress,
    IndexOf,
    Join,
)


def test_version():
    assert __version__ == "0.4.0"  # nosec B101


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


def test_split_raise():
    try:
        (Start(["clay,michelle"], raise_exception=True) > Split(","))
    except Exception as e:
        type(e).__name__ == "TypeError"


def test_split_no_raise():
    assert (  # nosec B101
        Start(["clay,michelle"]) > Split(",")
    ).result == "'list' object has no attribute 'split'"


def test_get_index():
    assert (  # nosec B101
        Start(["clay", "michelle"]) > GetIndex(1)
    ).result == "michelle"


def test_index_raise():
    try:
        (Start(Parser, raise_exception=True) > GetIndex(1))
    except Exception as e:
        assert type(e).__name__ == "TypeError"  # nosec B101


def test_index_no_raise():
    assert (  # nosec B101
        Start(Parser, raise_exception=False) > GetIndex(1)
    ).result == "'type' object is not subscriptable"


def test_chain1():
    assert (  # nosec B101
        Start("clay,michelle")
        > Base64Encode()
        > Base64Decode()
        > Split(",")
        > GetIndex(0)
        > ToUpper()
    ).result == "CLAY"


def test_history1():
    with open("tests/history1.json", "r") as f:
        golden = json.load(f)

    assert (  # nosec B101
        Start("Clay")
        > Base64Encode()
        > Base64Decode()
        > ToUpper()
        > Split("A")
        > GetIndex(0)
        > Concat(suffix="AY")
        > ToLower()
    ).history == golden


def test_base64encode_raise():
    try:
        (Start(["Clay"], raise_exception=True) > Base64Encode())
    except Exception as e:
        assert type(e).__name__ == "AttributeError"  # nosec B101


def test_base64encode():
    assert (  # nosec B101
        Start(["Clay"]) > Base64Encode()
    ).result == "'list' object has no attribute 'encode'"


def test_base64decode_raise():
    try:
        (Start(["Clay"], raise_exception=True) > Base64Decode())
    except Exception as e:
        assert type(e).__name__ == "TypeError"  # nosec B101


def test_base64decode():
    assert (  # nosec B101
        Start(["Clay"]) > Base64Decode()
    ).result == "argument should be a bytes-like object or ASCII string, not 'list'"


def test_to_upper_success():
    assert (Start("foobar") > ToUpper()).result == "FOOBAR"  # nosec B101


def test_to_upper_raise():
    try:
        (Start(["foobar"], raise_exception=True) > ToUpper())
    except Exception as e:
        assert type(e).__name__ == "AttributeError"  # nosec B101


def test_to_upper_fail():
    assert (  # nosec B101
        Start(["foobar"]) > ToUpper()
    ).result == "'list' object has no attribute 'upper'"


def test_get_field_success():
    assert (Start({"foo": "bar"}) > GetField("foo")).result == "bar"  # nosec B101


def test_get_field_raise():
    try:
        (Start(["foobar"], raise_exception=True) > GetField("foo"))
    except Exception as e:
        assert type(e).__name__ == "TypeError"  # nosec B101


def test_get_field_fail():
    assert (  # nosec B101
        Start(["foobar"]) > GetField("foo")
    ).result == "list indices must be integers or slices, not str"


def test_count_success():
    assert (Start({"foo": "bar"}) > Count()).result == 1  # nosec B101


def test_count_raise():
    try:
        (Start("", raise_exception=True) > Count())
    except Exception as e:
        assert type(e).__name__ == "TypeError"  # nosec B101


def test_count_fail():
    assert (  # nosec B101
        Start(Parser) > Count()
    ).result == "object of type 'type' has no len()"


def test_to_lower_success():
    assert (Start("FOOBAR") > ToLower()).result == "foobar"  # nosec B101


def test_to_lower_raise():
    try:
        (Start([], raise_exception=True) > ToLower())
    except Exception as e:
        assert type(e).__name__ == "AttributeError"  # nosec B101


def test_to_lower_fail():
    assert (  # nosec B101
        Start(Parser) > ToLower()
    ).result == "type object 'Parser' has no attribute 'lower'"


def test_ip_network_success():
    assert (  # nosec B101
        Start("192.168.1.55/24") > IpNetwork()
    ).result == "192.168.1.0/24"


def test_ip_network_raise():
    try:
        (Start("", raise_exception=True) > IpNetwork())
    except Exception as e:
        assert type(e).__name__ == "AddressValueError"  # nosec B101


def test_ip_network_fail():
    assert (Start("") > IpNetwork()).result == "Address cannot be empty"  # nosec B101


def test_regex_extract_success():
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


def test_regex_extract_success2():
    input_str = "I've got a lovely bunch of coconuts."
    pattern = r"coco(\S+)\."
    assert (Start(input_str) > RegexExtractAll(pattern)).result[  # nosec B101
        0
    ] == "nuts"


def test_regex_extract_raise():
    try:
        (Start([], raise_exception=True) > RegexExtractAll("asdf"))
    except Exception as e:
        assert type(e).__name__ == "TypeError"  # nosec B101


def test_regex_extract_fail():
    assert (  # nosec B101
        Start([]) > RegexExtractAll("asdf")
    ).result == "expected string or buffer"


def test_concat_success():
    assert (Start("baz") > Concat("foo", "bar")).result == "foobazbar"  # nosec B101


def test_concat_fail():
    assert (  # nosec B101
        Start([]) > Concat("foo", "bar")
    ).result == 'can only concatenate str (not "list") to str'


def test_concat_raise():
    try:
        (Start([], raise_exception=True) > Concat("foo", "bar"))
    except Exception as e:
        assert type(e).__name__ == "TypeError"  # nosec B101


def test_append_success():
    assert (Start("foo") > Append("bar")).result == "foobar"  # nosec B101


def test_append_fail():
    assert (  # nosec B101
        Start([]) > Append("bar")
    ).result == 'can only concatenate list (not "str") to list'


def test_append_raise():
    try:
        (Start([], raise_exception=True) > Append("bar"))
    except Exception as e:
        assert type(e).__name__ == "TypeError"  # nosec B101


def test_first_element_success():
    assert (Start(["foo", "bar"]) > FirstElement()).result == "foo"  # nosec B101


def test_first_element_fail():
    assert (  # nosec B101
        Start(Parser) > FirstElement()
    ).result == "'type' object is not subscriptable"


def test_first_element_raise():
    try:
        (Start("", raise_exception=True) > FirstElement())
    except Exception as e:
        assert type(e).__name__ == "IndexError"  # nosec B101


def test_last_element_success():
    assert (Start(["foo", "bar"]) > LastElement()).result == "bar"  # nosec B101


def test_last_element_fail():
    assert (  # nosec B101
        Start("") > LastElement()
    ).result == "string index out of range"


def test_last_element_raise():
    try:
        (Start("", raise_exception=True) > LastElement())
    except Exception as e:
        assert type(e).__name__ == "IndexError"  # nosec B101


def test_textfsm_success():
    with open(
        f"{os.path.dirname(os.path.realpath(__file__))}/templates/cisco_nxos_show_interfaces.textfsm",
        "r",
    ) as f:
        template = f.read()
    with open(
        f"{os.path.dirname(os.path.realpath(__file__))}/raw/cisco_nxos_show_interface.raw",
        "r",
    ) as f:
        input_data = f.read()
    with open(
        f"{os.path.dirname(os.path.realpath(__file__))}/golden/cisco_nxos_show_interface.json",
        "r",
    ) as f:
        golden = json.loads(f.read())

    assert (Start(input_data) > TextFSMParse(template)).result == golden  # nosec B101


def test_textfsm_success2():
    with open(
        f"{os.path.dirname(os.path.realpath(__file__))}/templates/cisco_nxos_show_interfaces.textfsm",
        "r",
    ) as f:
        template = f.read()
    with open(
        f"{os.path.dirname(os.path.realpath(__file__))}/raw/cisco_nxos_show_interface.raw",
        "r",
    ) as f:
        input_data = f.read()
    with open(
        f"{os.path.dirname(os.path.realpath(__file__))}/golden/cisco_nxos_show_interface_default.json",
        "r",
    ) as f:
        golden = json.loads(f.read())

    assert (  # nosec B101
        Start(input_data) > TextFSMParse(template, fmt="default")
    ).result == golden


def test_textfsm_fail():
    assert (  # nosec B101
        Start("") > TextFSMParse("")
    ).result == "Missing state 'Start'."


def test_textfsm_raise():
    with open(
        f"{os.path.dirname(os.path.realpath(__file__))}/templates/cisco_nxos_show_interfaces.textfsm",
        "r",
    ) as f:
        template = f.read()
    try:
        (Start("", raise_exception=True) > TextFSMParse(template))
    except Exception as e:
        assert type(e).__name__ == "TextFSMTemplateError"  # nosec B101


def test_textfsm_raise2():
    with open(
        f"{os.path.dirname(os.path.realpath(__file__))}/templates/cisco_nxos_show_interfaces.textfsm",
        "r",
    ) as f:
        template = f.read()
    try:
        (Start("", raise_exception=True) > TextFSMParse(template, fmt="default"))
    except Exception as e:
        assert type(e).__name__ == "TextFSMTemplateError"  # nosec B101


def test_macaddress_success():
    assert (  # nosec B101
        Start("0000.1111.2222") > MacAddress()
    ).result == "00:00:11:11:22:22"


def test_macaddress_fail():
    assert (  # nosec B101
        Start("0000.1111.ZZZZ") > MacAddress()
    ).result == "Invalid MAC address: 0000.1111.ZZZZ"


def test_macaddress_raise():
    try:
        (Start("0000.1111.2222", raise_exception=True) > MacAddress())
        (Start("0000.1111.ZZZZ", raise_exception=True) > MacAddress())
    except Exception as e:
        assert type(e).__name__ == "ValueError"  # nosec B101


def test_indexof_success():
    assert (Start(["foo", "bar"]) > IndexOf("foo")).result == 0  # nosec B101


def test_indexof_fail():
    assert (Start(["foo", "bar"]) > IndexOf("baz")).result == -1  # nosec B101
    try:
        (Start("foobar") > IndexOf("baz")).result
    except Exception as e:
        assert type(e).__name__ == "TypeError"  # nosec B101


def test_indexof_raise():
    try:
        (Start({"foo": "bar"}, raise_exception=True) > IndexOf("baz")).result
    except Exception as e:
        assert type(e).__name__ == "TypeError"  # nosec B101

    result = (Start(["foo", "bar"], raise_exception=True) > IndexOf("baz")).result
    assert result == -1  # nosec B101
    result = (Start(["foo", "bar"], raise_exception=True) > IndexOf("bar")).result
    assert result == 1  # nosec B101


def test_join():
    # success
    assert (Start(["a", "b", "c"]) > Join(",")).result == "a,b,c"  # nosec B101
    # fail
    assert (Start({"foo": "bar"}) > Join()).result == "Input must be list"  # nosec B101
    # raise
    try:
        (Start("foo", raise_exception=True) > Join())
    except Exception as e:
        assert type(e).__name__ == "TypeError"  # nosec B101
