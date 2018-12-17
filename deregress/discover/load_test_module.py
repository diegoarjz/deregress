import os
import importlib

from deregress.exceptions import InvalidTestsFile

def load_test_module_from_file(file_path):
    if not os.path.exists(file_path):
        raise InvalidTestsFile("Unable to find test file: %s" % file_path)

    file_name, extension = os.path.splitext(os.path.basename(file_path))

    if extension != ".py":
        raise InvalidTestsFile("File doesn't seem a valid python file: %s" % file_path)

    spec = importlib.util.spec_from_file_location(file_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
