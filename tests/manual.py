from knex.parsers import (
    Base64Decode,
    Base64Encode,
    GetIndex,
    Parser,
    Split,
    ToLower,
    ToUpper,
)

starter = Parser("foo,bar")
res = starter > Split(",") > GetIndex(1) > ToUpper()

print(res)
