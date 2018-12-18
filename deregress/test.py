import sys
import os
import shutil

from deregress.runner import Runner
from deregress.tester import Tester
from deregress.test_result import Result
from deregress.results_storage import ResultWriter, ResultReader, FileStorage

class TestsManager:
    managed_tests = []
    deregress_filename = "dregress.json"

    @staticmethod
    def add_managed_test(test):
        TestsManager.managed_tests.append(test)


    @staticmethod
    def get_managed_tests():
        return TestsManager.managed_tests


    def __init__(self):
        self._previous_test_results = None
        self._tests_to_run = TestsManager.get_managed_tests()
        self._make_reference = False
        self._deregress_dir = ".deregress"

    @property
    def make_reference(self):
        return self._make_reference

    @make_reference.setter
    def make_reference(self, value):
        self._make_reference = value

    @property
    def deregress_dir(self):
        return self._deregress_dir

    @deregress_dir.setter
    def deregress_dir(self, value):
        self._deregress_dir = value

    @property
    def deregress_file(self):
        return os.path.abspath(os.path.join(self._deregress_dir, TestsManager.deregress_filename))


    def initialize_deregress_dir(self, clean=False):
        if not os.path.exists(self.deregress_dir):
            os.mkdir(self.deregress_dir)
            return

        if clean:
            shutil.rmtree(self.deregress_dir)
            os.mkdir(self.deregress_dir)


    def load_previous_test_results(self):
        if os.path.exists(self.deregress_file):
            result_reader = ResultReader()
            result_reader.read(self.deregress_file)
            self._previous_test_results = result_reader.test_results


    def run_tests(self):
        single_test_count = 0
        file_storage = FileStorage(self.deregress_dir)
        result_writer = ResultWriter()

        for test in self._tests_to_run:
            test.tester.previous_test_results = self._previous_test_results
            test.tester.file_storage = file_storage
            test.tester.make_reference = self.make_reference

            results = test()

            for r in results:
                result_writer.add_test_result(r)
                single_test_count += 1

                if r.test_result == Result.Success:
                    sys.stdout.write(".")
                elif r.test_result == Result.Fail:
                    sys.stdout.write("F")
                elif r.test_result == Result.Error:
                    sys.stdout.write("E")
                elif r.test_result == Result.New:
                    sys.stdout.write("N")

                if single_test_count % 40 == 0:
                    sys.stdout.write("\n")

        if self.make_reference:
            result_writer.write(self.deregress_file)

        sys.stdout.write("\n")

        print("-"*70)
        print("Ran {} tests".format(single_test_count))


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

