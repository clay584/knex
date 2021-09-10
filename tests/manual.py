from knex.parsers import GetIndex, Parser, Split, ToUpper

starter = Parser("foo,bar")
res = starter > Split(",") > GetIndex(1) > ToUpper()

print(res)
