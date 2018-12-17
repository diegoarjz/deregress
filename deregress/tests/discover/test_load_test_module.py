import unittest
from unittest import mock

from deregress.discover import load_test_module
from deregress.exceptions import InvalidTestsFile

class TestLoadTestModule(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @mock.patch("deregress.discover.load_test_module.os.path.exists")
    def test_when_file_doesnt_exist_should_raise_exception(self, exists):
        exists.return_value = False
        with self.assertRaises(InvalidTestsFile):
            load_test_module.load_test_module_from_file("/non/existent/file.py")


    @mock.patch("deregress.discover.load_test_module.os.path.exists")
    def test_when_file_isnt_a_python_file_should_raise_exception(self, exists):
        exists.return_value = True

        with self.assertRaises(InvalidTestsFile):
            load_test_module.load_test_module_from_file("/not/python/file")


if __name__ == '__main__':
    unittest.main()
