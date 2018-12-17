import enum

class Result(enum.Enum):
    Success = "success"
    Fail = "fail"
    Error = "error"
    New = "new"

class TestResult:
    def __init__(self, name, test_result):
        self._name = name
        self._test_result = test_result
        self._result_value = None

    @property
    def name(self):
        return self._name

    @property
    def test_result(self):
        return self._test_result

    @property
    def result_value(self):
        return self._result_value

    @result_value.setter
    def result_value(self, value):
        self._result_value = value
