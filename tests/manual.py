from knex.parsers import Base64Decode, Base64Encode, GetIndex, Parser, Split


def test_gt():
    starter = Parser("clay,michelle")
    print(starter)
    print(starter > Base64Encode())
    print(
        starter
        > Base64Encode()
        > Base64Decode()
        > Split(delimeter=",")
        > GetIndex(idx=2)
    )


test_gt()
