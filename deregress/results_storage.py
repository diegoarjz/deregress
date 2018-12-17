import json
import os

from deregress.test_result import *

class TestResultEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, TestResult):
            return {
                "_type": TestResult.__name__,
                "name" : obj.name,
                "result": obj.test_result.value,
                "value": obj.result_value
            }
        return super(TestResultEncoder, self).default(obj)


class ResultWriter:
    def __init__(self):
        self._test_results = []

    def add_test_result(self, test_result: TestResult):
        self._test_results.append(test_result)

    def write(self, out_file):
        json_string = json.dumps(self._test_results, cls=TestResultEncoder, indent=2)
        with open(out_file, "w") as f:
            f.write(json_string)


class TestResultDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        if "_type" not in obj:
            return obj

        type = obj["_type"]
        if type == TestResult.__name__:
            test_result = TestResult(obj["name"], Result(obj["result"]))
            test_result.result_value = obj["value"]
            return test_result
        return obj


class ResultReader:
    def __init__(self):
        self._test_results = {}


    @property
    def test_results(self):
        return self._test_results

    def read(self, in_file):
        if not os.path.exists(in_file):
            return

        input_json = open(in_file, "r").read()
        read_results = json.loads(input_json, cls=TestResultDecoder)

        for r in read_results:
            self._test_results[r.name] = r
