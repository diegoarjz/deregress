import sys
import os

from deregress.runner import Runner
from deregress.tester import Tester
from deregress.test_result import Result
from deregress.results_storage import ResultWriter, ResultReader

class TestsManager:
    managed_tests = []

    @staticmethod
    def add_managed_test(test):
        TestsManager.managed_tests.append(test)


    @staticmethod
    def get_managed_tests():
        return TestsManager.managed_tests


    def __init__(self):
        self._previous_test_results = None
        self._tests_to_run = TestsManager.get_managed_tests()


    def load_previous_test_results(self):
        if os.path.exists("deregress.json"):
            result_reader = ResultReader()
            result_reader.read("deregress.json")
            self._previous_test_results = result_reader.test_results


    def run_tests(self):
        single_test_count = 0
        for test in self._tests_to_run:
            test.tester.previous_test_results = self._previous_test_results
            results = test()
            single_test_count += len(results)

            for r in results:
                if r.test_result == Result.Success:
                    sys.stdout.write(".")
                elif r.test_result == Result.Fail:
                    sys.stdout.write("F")
                elif r.test_result == Result.Error:
                    sys.stdout.write("E")
                elif r.test_result == Result.New:
                    sys.stdout.write("N")

        sys.stdout.write("\n")

        print("-"*70)
        print("Ran {} tests".format(single_test_count))

    def make_reference(self):
        result_writer = ResultWriter()
        for test in self._tests_to_run:
            results = test.results
            for result in results:
                result_writer.add_test_result(result)
        result_writer.write("deregress.json")


class TestWrapper:
    def __init__(self, wrapped_test):
        self._wrapped = wrapped_test
        self._runner = Runner()
        self._tester = Tester(self.name)

        TestsManager.add_managed_test(self)


    def __call__(self, *args):
        self._wrapped(self)
        return self._tester.test_results


    @property
    def runner(self):
        return self._runner

    @property
    def tester(self):
        return self._tester

    @property
    def name(self):
        return "{}.{}".format(self._wrapped.__module__, self._wrapped.__name__)

    @property
    def results(self):
        return self._tester.test_results


def decorator(func):
    return TestWrapper(func)

