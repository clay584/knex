from knex.parsers import Base64Decode, Base64Encode, Parser


def test_gt():
    starter = Parser("clay")
    encode = Base64Encode()
    decode = Base64Decode()
    print(starter > encode > decode)


test_gt()
