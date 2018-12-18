import os
import hashlib
import inspect
import filecmp

from deregress.test_result import *

def md5Checksum(filePath):
    with open(filePath, 'rb') as fh:
        m = hashlib.md5()
        while True:
            data = fh.read(8192)
            if not data:
                break
            m.update(data)
        return m.hexdigest()


def test_assertion(func):
    def wrapper(*args, **kwargs):
        Self = args[0]

        argspec = inspect.signature(func).parameters
        arg_names = [param for param in argspec]

        call_args = {}
        argspec_index = 1
        for arg in args[1:]:
            call_args[arg_names[argspec_index]] = arg
            argspec_index += 1

        for arg_name in arg_names[argspec_index:]:
            call_args[arg_name] = kwargs[arg_name]

        name = "{}.{}.{}".format(
                    Self._basename,
                    func.__name__, 
                    "&".join([str("{}={}".format(arg, call_args[arg])) for arg in call_args]))

        if Self._previous_test_results is not None and name in Self._previous_test_results:
            Self._result_for_current_test = Self._previous_test_results[name]
        else:
            Self._result_for_current_test = None

        result, value = func(*args, **kwargs)

        test_result = TestResult(name, result)
        test_result.result_value = value
        Self._test_results.append(test_result)

        Self._result_for_current_test = None

        return test_result
    return wrapper


class Tester:
    def __init__(self, basename):
        self._basename = basename
        self._test_results = []
        self._previous_test_results = None
        self._result_for_current_test = None


    @property
    def test_results(self):
        return self._test_results

    @property
    def previous_test_results(self):
        return self._previous_test_results

    @previous_test_results.setter
    def previous_test_results(self, value):
        self._previous_test_results = value

    @test_assertion
    def file_should_exist(self, file_path):
        file_exists = os.path.exists(file_path)
        return Result.Success if file_exists else Result.Fail, file_exists

    @test_assertion
    def file_contents_should_match(self, file_path):
        if not os.path.exists(file_path):
            return Result.Error, None

        if self._result_for_current_test is not None:
            prev_file_path = self._result_for_current_test.result_value
            if filecmp.cmp(prev_file_path, file_path):
                return Result.Success, file_path
            else:
                return Result.Fail, file_path
        else:
            return Result.New, file_path


    @test_assertion
    def file_hash_should_match(self, file_path):
        if not os.path.exists(file_path):
            return Result.Error, None

        test_result = None
        file_hash = md5Checksum(file_path)

        if self._result_for_current_test is not None:
            prev_value = self._result_for_current_test.result_value

            if prev_value != file_hash:
                test_result = Result.Fail
            else:
                test_result = Result.Success
        else:
            test_result = Result.New

        return test_result, file_hash
