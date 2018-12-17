
class InvalidTestsFile(Exception):
    def __init__(self, message):
        super().__init__(message)


class InvalidExecutable(Exception):
    def __init__(self, message):
        super().__init__(message)
