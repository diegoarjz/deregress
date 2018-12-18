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

    @mock.patch("deregress.tester.filecmp.cmp", autospec=True)
    def test_when_testing_if_file_contents_match_and_they_do_should_add_successful_test_result(self, mock_filecmp):
        self.mock_exists.return_value = True
        mock_filecmp.return_value = True
        test_result = TestResult("result", Result.Success)
        test_result.result_value = "exists"
        self.tester.previous_test_results = {
            "basename.file_contents_should_match.file_path=exists": test_result
        }

        result = self.tester.file_contents_should_match("exists")
        mock_filecmp.assert_called_with("exists", "exists")
        self.assertEqual(result.name, "basename.file_contents_should_match.file_path=exists")
        self.assertEqual(result.test_result, Result.Success)

    @mock.patch("deregress.tester.filecmp.cmp", autospec=True)
    def test_when_testing_if_file_contents_match_and_they_dont_should_add_failed_test_result(self, mock_filecmp):
        self.mock_exists.return_value = True
        mock_filecmp.return_value = False
        test_result = TestResult("result", Result.Success)
        test_result.result_value = "exists"
        self.tester.previous_test_results = {
            "basename.file_contents_should_match.file_path=exists": test_result
        }

        result = self.tester.file_contents_should_match("exists")
        mock_filecmp.assert_called_with("exists", "exists")
        self.assertEqual(result.name, "basename.file_contents_should_match.file_path=exists")
        self.assertEqual(result.test_result, Result.Fail)

    def test_when_testing_if_file_contents_match_but_file_doesnt_exist_should_add_error_test_result(self):
        self.mock_exists.return_value = False
        result = self.tester.file_contents_should_match("exists")
        self.assertEqual(result.test_result, Result.Error)

    def test_when_testing_if_file_contents_match_but_there_is_no_previous_result_should_add_new_test_result(self):
        self.mock_exists.return_value = True
        result = self.tester.file_contents_should_match("exists")
        self.assertEqual(result.test_result, Result.New)

    @mock.patch("deregress.tester.md5Checksum", autospec=True)
    def test_when_testing_if_file_hash_match_and_it_does_should_add_successful_test_result(self, mock_md5Checksum):
        self.mock_exists.return_value = True
        mock_md5Checksum.return_value = "md5_hash"
        test_result = TestResult("result", Result.Success)
        test_result.result_value = "md5_hash"
        self.tester.previous_test_results = {
            "basename.file_hash_should_match.file_path=exists": test_result
        }

        result = self.tester.file_hash_should_match("exists")
        mock_md5Checksum.assert_called_with("exists")
        self.assertEqual(result.name, "basename.file_hash_should_match.file_path=exists")
        self.assertEqual(result.test_result, Result.Success)

    @mock.patch("deregress.tester.md5Checksum", autospec=True)
    def test_when_testing_if_file_hash_match_but_it_doesnt_should_add_failed_test_result(self, mock_md5Checksum):
        self.mock_exists.return_value = True
        mock_md5Checksum.return_value = "md0_hash"
        test_result = TestResult("result", Result.Success)
        test_result.result_value = "md5_hash"
        self.tester.previous_test_results = {
            "basename.file_hash_should_match.file_path=exists": test_result
        }

        result = self.tester.file_hash_should_match("exists")
        mock_md5Checksum.assert_called_with("exists")
        self.assertEqual(result.name, "basename.file_hash_should_match.file_path=exists")
        self.assertEqual(result.test_result, Result.Fail)

    @mock.patch("deregress.tester.md5Checksum", autospec=True)
    def test_when_testing_if_file_hash_match_but_file_doesnt_exist_should_add_error_test_result(self, mock_md5Checksum):
        self.mock_exists.return_value = False
        mock_md5Checksum.return_value = "md0_hash"
        result = self.tester.file_hash_should_match("exists")
        self.assertEqual(result.test_result, Result.Error)

    @mock.patch("deregress.tester.md5Checksum", autospec=True)
    def test_when_testing_if_file_hash_match_but_there_isnt_a_previous_test_should_add_new_test_result(self, mock_md5Checksum):
        self.mock_exists.return_value = True
        mock_md5Checksum.return_value = "md5_hash"
        result = self.tester.file_hash_should_match("exists")
        self.assertEqual(result.test_result, Result.New)


if __name__ == '__main__':
    unittest.main()

