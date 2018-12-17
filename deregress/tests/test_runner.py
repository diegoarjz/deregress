import unittest
from unittest import mock
import os

from . import utils

from deregress.runner import Runner
from deregress.exceptions import InvalidExecutable


class TestRunner(unittest.TestCase):
    def setUp(self):
        self.runner = Runner()
        self.path_to_executable = "path/to/executable"
        self.path_to_stdout = "path/to/stdout"
        self.path_to_stderr = "path/to/stderr"

        self.mock_exists = utils.mock_for_all_tests(self, "deregress.runner.os.path.exists")
        self.mock_access = utils.mock_for_all_tests(self, "deregress.runner.os.access")

        self.mock_exists.return_value = True
        self.mock_access.return_value = True

    def tearDown(self):
        pass


    @mock.patch("deregress.runner.Popen", autospec=True)
    def test_when_running_a_command_should_call_Popen(self, mock_Popen):
        self.runner.executable(self.path_to_executable).run()
        mock_Popen.assert_called_with([self.path_to_executable])


    def test_when_executable_doesnt_exist_should_raise_exception(self):
        self.mock_exists.return_value = False
        with self.assertRaises(InvalidExecutable):
            self.runner.executable("doesnt/exist").run()


    @mock.patch("deregress.runner.Popen", autospec=True)
    def test_when_running_should_test_if_file_is_executable(self, mock_Popen):
        self.runner.executable(self.path_to_executable).run()
        self.mock_access.assert_called_with(self.path_to_executable, os.X_OK)


    def test_when_executable_doesnt_have_executable_permissions_should_raise_exception(self):
        self.mock_exists.return_value = False
        with self.assertRaises(InvalidExecutable):
            self.runner.executable("not/executable").run()


    @mock.patch("deregress.runner.Popen", autospec=True)
    def test_when_running_with_arguments_should_pass_arguments_to_Popen(self, mock_Popen):
        self.runner \
                .executable(self.path_to_executable) \
                .arg("arg1") \
                .arg("arg2") \
                .run()
        mock_Popen.assert_called_with([
            self.path_to_executable, "arg1", "arg2"
        ])


    @mock.patch("deregress.runner.Popen", autospec=True)
    def test_when_calling_with_multiple_arguments_should_pass_all_to_Popen(self, mock_Popen):
        self.runner \
                .executable(self.path_to_executable) \
                .args(["arg1", "arg2"]) \
                .run()
        mock_Popen.assert_called_with([
            self.path_to_executable, "arg1", "arg2"
        ])


    @mock.patch("deregress.runner.open")
    @mock.patch("deregress.runner.Popen", autospec=True)
    def test_when_redirecting_stdout_should_save_to_file(self, mock_Popen, mock_open):
        opened_file = mock_open.return_value 
        self.runner \
                .executable(self.path_to_executable) \
                .stdout(self.path_to_stdout) \
                .run()
        mock_open.assert_called_with(self.path_to_stdout, "wb")
        mock_Popen.assert_called_with(
                [self.path_to_executable],
                stdout=opened_file
        )


    @mock.patch("deregress.runner.open")
    @mock.patch("deregress.runner.Popen", autospec=True)
    def test_when_redirecting_stderr_should_save_to_file(self, mock_Popen, mock_open):
        opened_file = mock_open.return_value 
        self.runner \
                .executable(self.path_to_executable) \
                .stderr(self.path_to_stderr) \
                .run()
        mock_open.assert_called_with(self.path_to_stderr, "wb")
        mock_Popen.assert_called_with(
                [self.path_to_executable],
                stderr=opened_file
        )


if __name__ == '__main__':
    unittest.main()
