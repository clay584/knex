import base64


class Parser:
    def __init__(self, input=None):
        self.input = input

    def process(self):
        return self.input

    def __gt__(self, other):
        other.input = self.process()
        return other.process()


class Base64Encode(Parser):
    def process(self):
        return base64.b64encode(self.input.encode())


class Base64Decode(Parser):
    def process(self):
        return base64.b64decode(self.input).decode()
