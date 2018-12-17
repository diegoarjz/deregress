# deregress

deregress aims to be a lightweight regression testing system suitable to be used in open source projects.

The idea is to provide an easy way to define tests that run executables and assert conditions on its output (e.g.,
files, stdout and stderr), comparing them to the output of a previous run that was marked as a reference. The tests are
specified in simple python functions and are automatically run by deregress.

You can submit the tests file along with the source code for your project and other contributors will be able to
implement new features while being sure that they are not breaking others.

# Installing and Using deregress

To install, simply run `pip install`:

```
$ pip install deregress
```

Then define the tests in a file. This is done by using the deregress.test decorator which injects a test object into a
function which, in turn, exposes a runner and a tester object.

The runner object allows to run the executable under test with specific command line arguments. The tester object
verifies whether certain conditions have been met. The results of these conditions can be saved into a file which is
later used to check for regressions.

For example, the next file runs the executable in `path/to/executable` with the `--out-file=file.txt` argument,
indicating that the file.txt will be created. Then, two tests are made on the results. The first tests whether
`file.txt` exists and the second checks if the file md5 hash has changed from a previous run.

```python
import deregress

# Define a test in deregress
@deregress.test
def test_1(test):
    # run the executable with the given arguments
    test.runner.run("path/to/executable") \
        .arg("--out-file=file.txt") \
        .run()

    test.tester.file_should_exist("file.txt")
    test.tester.file_hash_should_match("file.txt")
```

To run the tests in a test file you need to run deregress as a python module and provide the path to the test file:

```
$ python -m deregress --run=tests.py
```

To mark the results of a run as a reference for posterior runs, you can run the following in a command line:

```
$ python -m deregress --run=tests.py --make-referece
```

Note that (currently) this will overwrite the previous file.
