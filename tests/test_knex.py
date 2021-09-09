from knex import __version__
from knex.parsers import Base64Encode, Parser


def test_version():
    assert __version__ == "0.1.1"  # nosec B101


def test_gt():
    p1 = Parser()
    p1.name = "p1"
    p2 = Parser()
    p2.name = "p2"
    print(p1 > p2)
