import json

DEFAULT_ERROR = "Oops! Florent suffered from an internal server error."

class FlorentError(Exception):
    def __init__(self, msg, code=400):
        self.msg = msg
        self.code = code

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "Code: {code} - {msg}".format(
            msg=self.msg,
            code=self.code
        )

    def to_json(self):
        return json.dumps({
            "code": self.code,
            "error": self.msg
        })
