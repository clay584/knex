from knex.parsers import Base64Decode, Base64Encode, Parser


def test_gt():
    starter = Parser("clay")
    print(starter)
    print(starter > Base64Encode())
    print(starter > Base64Encode() > Base64Decode())


test_gt()
