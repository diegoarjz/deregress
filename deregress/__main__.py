import argparse

from deregress.discover.load_test_module import *
from deregress.test import TestsManager


def _command_line_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--run", help="Run specified files")
    parser.add_argument("--make-reference", action="store_true",
            help="Marks the results of the run as the next reference")
    parser.add_argument("--clean-references", action="store_true",
            help="Deletes all previous references before running the tests")

    return parser


def main():
    parser = _command_line_args()
    args = parser.parse_args()

    if args.run is not None:
        load_test_module_from_file(args.run)

    test_manager = TestsManager()

    test_manager.initialize_deregress_dir(clean=args.clean_references)
    test_manager.make_reference = args.make_reference
    test_manager.load_previous_test_results()
    test_manager.run_tests()

if __name__ == '__main__':
    main()
