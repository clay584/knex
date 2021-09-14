import json

from knex.parsers import (
    Base64Decode,
    Base64Encode,
    Concat,
    GetIndex,
    Split,
    Start,
    ToLower,
    ToUpper,
)

# end = Start("foo,bar") > Split(",") > GetIndex(1) > ToUpper()
# print(json.dumps(end.history, indent=4))
# base = Base64Encode()

print(
    json.dumps(
        (
            Start("Clay")
            > Base64Encode()
            > Base64Decode()
            > ToUpper()
            > Split("A")
            > GetIndex(0)
            > Concat(suffix="AY")
            > ToLower()
        ).history,
        indent=4,
    )
)

# end = start > Base64Encode() > Base64Decode()
# print(end.result)
# print(end)
# print(json.dumps(end.result, indent=4))

# print(end)

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
# starter = Parser(output)
# pattern = r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"
# ender = starter > RegexExtractAll(pattern)

# print(json.dumps(ender.result, indent=4))
# print(ender)
