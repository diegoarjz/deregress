import unittest
from unittest import mock

from . import utils

from deregress.tester import Tester
from deregress.test_result import *

class TestTester(unittest.TestCase):
    def setUp(self):
        self.tester = Tester("basename")

        self.mock_exists = utils.mock_for_all_tests(self, "deregress.tester.os.path.exists")

    def tearDown(self):
        pass


    def test_when_testing_if_file_exists_and_it_does_should_add_successful_test_result(self):
        self.mock_exists.return_value = True
        result = self.tester.file_should_exist("exists")
        self.mock_exists.assert_called_with("exists")
        self.assertEqual(result.name, "basename.file_should_exist.file_path=exists")
        self.assertEqual(result.test_result, Result.Success)


    def test_when_testing_if_file_exists_and_it_doesnt_should_add_failed_test_result(self):
        self.mock_exists.return_value = False
        result = self.tester.file_should_exist(file_path="exists")
        self.mock_exists.assert_called_with("exists")
        self.assertEqual(result.name, "basename.file_should_exist.file_path=exists")
        self.assertEqual(result.test_result, Result.Fail)

    def test_when_testing_if_file_contents_match_and_they_do_should_add_successful_test_result(self):
        pass

    def test_when_testing_if_file_contents_match_and_they_dont_should_add_failed_test_result(self):
        pass

    def test_when_testing_if_file_contents_match_but_file_doesnt_exist_should_add_error_test_result(self):
        pass

    def test_when_testing_if_file_hash_match_and_it_does_should_add_successful_test_result(self):
        pass

    def test_when_testing_if_file_hash_match_but_it_doesnt_should_add_failed_test_result(self):
        pass

    def test_when_testing_if_file_hash_match_but_file_doesnt_exist_should_add_error_test_result(self):
        pass


if __name__ == '__main__':
    unittest.main()

