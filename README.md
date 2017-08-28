# `pytest_generate_tests` conflicts with `conftest.py` fixtures

This repository provides examples of how pytest allows parametrization of tests via
`pytest_generate_tests` and shall illustrate two issues:

- pytest failing with `duplicate values` during test collection phase
- pytest collecting too many test cases

The repository also shows workarounds using dumb fixture hiding the one from `conftest.py`:

- preventing `duplicate values` error
- preventing too many collected tests

## Concepts

Motivation is to run a test case, which has two parameters:

- dataset
- loc_id

The challange is, that there are more `loc_id` values to test with one dataset and that there are
multiple datasets, each having different `loc_id` values to test.

There are 6 separate test suites:

- tests/000_testparams/
- tests/001_onefile_fix/
- tests/002_onefile_gen/
- tests/003_conftest_fixt1/
- tests/004_conftest_fixt1_fix/
- tests/005_conftest_fixt2/
- tests/006_conftest_fixt2_fix/

Do not attempt to run tests for all the suites at once, this will fail (conflicting `test_it.py` in
multiple directories.)

```bash
$ py.test -sv 
============================= test session starts ==============================
platform linux -- Python 3.6.1, pytest-3.2.1, py-1.4.34, pluggy-0.4.0 -- /home/javl/.pyenv/versions/3.6.1/bin/python3.6
cachedir: .cache
rootdir: /home/javl/sandbox/generate_tests, inifile:
collecting ... collected 4 items / 6 errors

==================================== ERRORS ====================================
______________ ERROR collecting tests/001_onefile_fix/test_it.py _______________
import file mismatch:
imported module 'test_it' has this __file__ attribute:
  /home/javl/sandbox/generate_tests/tests/000_testparams/test_it.py
which is not the same as the test file we want to collect:
  /home/javl/sandbox/generate_tests/tests/001_onefile_fix/test_it.py
HINT: remove __pycache__ / .pyc files and/or use a unique basename for your test file modules
______________ ERROR collecting tests/002_onefile_gen/test_it.py _______________
...
...
...
!!!!!!!!!!!!!!!!!!! Interrupted: 6 errors during collection !!!!!!!!!!!!!!!!!!!!
=========================== 6 error in 0.10 seconds ============================
```

The only way to run the tests is to collect from one directory only:

```bash
$ py.test -sv tests/000_testparams
============================= test session starts ==============================
platform linux -- Python 3.6.1, pytest-3.2.1, py-1.4.34, pluggy-0.4.0 -- /home/javl/.pyenv/versions/3.6.1/bin/python3.6
cachedir: .cache
rootdir: /home/javl/sandbox/generate_tests, inifile:
collecting ... collected 4 items

tests/000_testparams/test_it.py::test_it[SET_01-loc_a] dataset, loc_id SET_01 loc_a
PASSED
tests/000_testparams/test_it.py::test_it[SET_01-loc_b] dataset, loc_id SET_01 loc_b
PASSED
tests/000_testparams/test_it.py::test_it[SET_02-loc_a] dataset, loc_id SET_02 loc_a
PASSED
tests/000_testparams/test_it.py::test_it[SET_02-loc_b] dataset, loc_id SET_02 loc_b
PASSED

=========================== 4 passed in 0.01 seconds ===========================
```
## Installation and execution

One can run all the tests using `tox`.

```bash
$ tox
```

To run specific tests manually:

- cretate virtualenv and activate it
- install `pytest` and optionally `pdbpp`
- run the test by ```$ py.test -sv tests/{test_directory}```


## Test suites

### 000_testparams: single test file with parametrized test case

Following `tests/000_testparams/test_it.py` illustrates the test case:

```python
import pytest

DATASET_NAMES = ["SET_01", "SET_02"]
LOC_NAMES = ["loc_a", "loc_b"]


PARAMS = [(set_name, loc_id)
        for set_name in DATASET_NAMES
        for loc_id in LOC_NAMES]


@pytest.mark.parametrize("dataset,loc_id", PARAMS)
def test_it(dataset, loc_id):
    print("dataset, loc_id", dataset, loc_id)
```

It shall generally run a test `test_it` for combination of dataset names and loc_ids.

For sake of simplicity, each data set has the same set of locations (real scenario was more complex
and locations were different for each data set).


Running the test we see all runs well:

```bash
$ py.test -sv tests/000_testparams/
============================= test session starts ==============================
platform linux -- Python 3.6.1, pytest-3.2.1, py-1.4.34, pluggy-0.4.0 -- /home/javl/.pyenv/versions/3.6.1/bin/python3.6
cachedir: .cache
rootdir: /home/javl/sandbox/generate_tests, inifile:
collecting ... collected 4 items

tests/000_testparams/test_it.py::test_it[SET_01-loc_a] dataset, loc_id SET_01 loc_a
PASSED
tests/000_testparams/test_it.py::test_it[SET_01-loc_b] dataset, loc_id SET_01 loc_b
PASSED
tests/000_testparams/test_it.py::test_it[SET_02-loc_a] dataset, loc_id SET_02 loc_a
PASSED
tests/000_testparams/test_it.py::test_it[SET_02-loc_b] dataset, loc_id SET_02 loc_b
PASSED

=========================== 4 passed in 0.01 seconds ===========================
```

Note the "test id" shown in square brackets (e.g. `[SET_01-loc_a]`). The text inside shows what
fixture instances are participating in given test run.

### 001_onefile_fix: single file using one fixture

This case acomplish the parametrization by means of fixtures:

- dataset
- loc_id

The fixtures are parametrized and tests case is run for all possible combinations of fixture values.

```python
import pytest

DATASET_NAMES = ["SET_01", "SET_02"]
LOC_NAMES = ["loc_a", "loc_b"]


@pytest.fixture(scope="session", params=DATASET_NAMES)
def dataset(request):
    return request.param


@pytest.fixture(scope="session", params=LOC_NAMES)
def loc_id(request):
    return request.param


def test_it(dataset, loc_id):
    print("dataset, loc_id", dataset, loc_id)
```

Running the tests we see, all runs well:

```bash
$ py.test -sv tests/001_onefile_fix
============================= test session starts ==============================
platform linux -- Python 3.6.1, pytest-3.2.1, py-1.4.34, pluggy-0.4.0 -- /home/javl/.pyenv/versions/3.6.1/bin/python3.6
cachedir: .cache
rootdir: /home/javl/sandbox/generate_tests, inifile:
collecting ... collected 4 items

tests/001_onefile_fix/test_it.py::test_it[SET_01-loc_a] dataset, loc_id SET_01 loc_a
PASSED
tests/001_onefile_fix/test_it.py::test_it[SET_01-loc_b] dataset, loc_id SET_01 loc_b
PASSED
tests/001_onefile_fix/test_it.py::test_it[SET_02-loc_b] dataset, loc_id SET_02 loc_b
PASSED
tests/001_onefile_fix/test_it.py::test_it[SET_02-loc_a] dataset, loc_id SET_02 loc_a
PASSED

=========================== 4 passed in 0.01 seconds ===========================
```

### 002_onefile_gen: single file using `pytest_generate_tests`

This time we parametrize by means of `pytest_generate_tests` function, which builds up
arguments to pass into test. It seems complicated, but it is actually the only method to resolve
more complex scenarios (e.g. multiple data sets, each having different loc_id values).

```python
import pytest

DATASET_NAMES = ["SET_01", "SET_02"]
LOC_NAMES = ["loc_a", "loc_b"]


def pytest_generate_tests(metafunc):
    dataset_names = DATASET_NAMES
    argnames = "dataset,loc_id"
    args_lst = []
    for dataset in dataset_names:
        for loc_id in LOC_NAMES:
            args_lst.append([dataset, loc_id])
    metafunc.parametrize(argnames, args_lst)


def test_it(dataset, loc_id):
    print("dataset,loc_id", dataset, loc_id)
```

Running the test we see all runs well:
```bash
$ py.test -sv tests/002_onefile_gen
============================= test session starts ==============================
platform linux -- Python 3.6.1, pytest-3.2.1, py-1.4.34, pluggy-0.4.0 -- /home/javl/.pyenv/versions/3.6.1/bin/python3.6
cachedir: .cache
rootdir: /home/javl/sandbox/generate_tests, inifile:
collecting ... collected 4 items

tests/002_onefile_gen/test_it.py::test_it[SET_01-loc_a] dataset,loc_id SET_01 loc_a
PASSED
tests/002_onefile_gen/test_it.py::test_it[SET_01-loc_b] dataset,loc_id SET_01 loc_b
PASSED
tests/002_onefile_gen/test_it.py::test_it[SET_02-loc_a] dataset,loc_id SET_02 loc_a
PASSED
tests/002_onefile_gen/test_it.py::test_it[SET_02-loc_b] dataset,loc_id SET_02 loc_b
PASSED

=========================== 4 passed in 0.01 seconds ===========================
```

### 003_conftest_fixt1: test file + `conftest.py` with one fixture (duplicate values)

This time we introduce `conftest.py` and define here a fixture `dataset`. Important things are:

- `conftest.py` fixture has the same name as our test case paramater `dataset`
- `conftest.py` fixture `dataset` is inentionaly using different dataset names.
- `conftest.py` fixture is not supposed to be used by our test case as `pytest_generate_tests` shall
  assigne different value

Note, that defining fixture in `conftest.py` and then selectively using or overriding it in specific
test files is standard technique for `py.test` framework. The purpose of this experiment is to make
sure, it works well in our case too.

```python
import pytest


DATASET_NAMES = ["alfa", "beta", "gama"]


@pytest.fixture(scope="session", params=DATASET_NAMES)
def dataset(request):
    return request.param
```

Running the tests we see a problem:

```bash
$ py.test -sv tests/003_conftest_fixt1
============================= test session starts ==============================
platform linux -- Python 3.6.1, pytest-3.2.1, py-1.4.34, pluggy-0.4.0 -- /home/javl/.pyenv/versions/3.6.1/bin/python3.6
cachedir: .cache
rootdir: /home/javl/sandbox/generate_tests, inifile:
collecting ... collected 0 items / 1 errors

==================================== ERRORS ====================================
_____________ ERROR collecting tests/003_conftest_fixt1/test_it.py _____________
../../.pyenv/versions/3.6.1/lib/python3.6/site-packages/_pytest/runner.py:196: in __init__
    self.result = func()
...
...
...
../../.pyenv/versions/3.6.1/lib/python3.6/site-packages/_pytest/python.py:682: in setmulti
    self._checkargnotcontained(arg)
../../.pyenv/versions/3.6.1/lib/python3.6/site-packages/_pytest/python.py:665: in _checkargnotcontained
    raise ValueError("duplicate %r" % (arg,))
E   ValueError: duplicate 'dataset'
!!!!!!!!!!!!!!!!!!! Interrupted: 1 errors during collection !!!!!!!!!!!!!!!!!!!!
=========================== 1 error in 0.32 seconds ============================
```

It seems as the pytest collector is confused and did not recognize, that the test case already got
the parameter from `pytest_generate_tests` which shall override any value provided by other
fixtures. Currently I consider this a bug in `pytest`.

### 004_conftest_fixt1_fix: test file + `conftest.py` with one fixture (fixed)

This test case is fixing the conflict `ValueError: duplicate 'dataset'` by adding dummy fixture
into test file.
```python
import pytest

DATASET_NAMES = ["SET_01", "SET_02"]
LOC_NAMES = ["loc_a", "loc_b"]


@pytest.fixture(scope="session")
def dataset():
    return "to-be-ignored"

def pytest_generate_tests(metafunc):
    dataset_names = DATASET_NAMES
    argnames = "dataset,loc_id"
    args_lst = []
    for dataset in dataset_names:
        for loc_id in LOC_NAMES:
            args_lst.append([dataset, loc_id])
    metafunc.parametrize(argnames, args_lst)


def test_it(dataset, loc_id):
    print("dataset,loc_id", dataset, loc_id)
```
The idea is to hide `conftest.py` provided fixture by dummy fixture and let `pytest_generate_tests`
do it's own work with real fixture value calculated inside of this function.

Running the tests we see, the problem is resolved:
```bash
$ py.test -sv tests/004_conftest_fixt1_fix
============================= test session starts ==============================
platform linux -- Python 3.6.1, pytest-3.2.1, py-1.4.34, pluggy-0.4.0 -- /home/javl/.pyenv/versions/3.6.1/bin/python3.6
cachedir: .cache
rootdir: /home/javl/sandbox/generate_tests, inifile:
collecting ... collected 4 items

tests/004_conftest_fixt1_fix/test_it.py::test_it[SET_01-loc_a] dataset,loc_id SET_01 loc_a
PASSED
tests/004_conftest_fixt1_fix/test_it.py::test_it[SET_01-loc_b] dataset,loc_id SET_01 loc_b
PASSED
tests/004_conftest_fixt1_fix/test_it.py::test_it[SET_02-loc_a] dataset,loc_id SET_02 loc_a
PASSED
tests/004_conftest_fixt1_fix/test_it.py::test_it[SET_02-loc_b] dataset,loc_id SET_02 loc_b
PASSED

=========================== 4 passed in 0.01 seconds ===========================
```

### 005_conftest_fixt2: test file + `conftest.py` with dependent fixtures (duplicate tests)

This illustrattes another issue: collecting more test cases, than is really expected.

The `test_it.py` is as in `003_conftest_fixt1` (thus no dummy fixture present).

The `conftest.py` gets `dataset` fixture calculated from value of another fixture `dataset_name`.
```python
import pytest


DATASET_NAMES = ["alfa", "beta", "gama"]


@pytest.fixture(scope="module", params=DATASET_NAMES)
def dataset_name(request):
    return request.param


@pytest.fixture(scope="session")
def dataset(dataset_name):
    return dataset_name
```
Running the test we see, all runs, but closer look to number of tests run is surprising:

```bash
$ py.test -sv tests/005_conftest_fixt2
============================= test session starts ==============================
platform linux -- Python 3.6.1, pytest-3.2.1, py-1.4.34, pluggy-0.4.0 -- /home/javl/.pyenv/versions/3.6.1/bin/python3.6
cachedir: .cache
rootdir: /home/javl/sandbox/generate_tests, inifile:
collecting ... collected 12 items

tests/005_conftest_fixt2/test_it.py::test_it[SET_01-loc_a-alfa] dataset,loc_id SET_01 loc_a
PASSED
tests/005_conftest_fixt2/test_it.py::test_it[SET_01-loc_b-alfa] dataset,loc_id SET_01 loc_b
PASSED
tests/005_conftest_fixt2/test_it.py::test_it[SET_02-loc_a-alfa] dataset,loc_id SET_02 loc_a
PASSED
tests/005_conftest_fixt2/test_it.py::test_it[SET_02-loc_b-alfa] dataset,loc_id SET_02 loc_b
PASSED
tests/005_conftest_fixt2/test_it.py::test_it[SET_01-loc_a-beta] dataset,loc_id SET_01 loc_a
PASSED
tests/005_conftest_fixt2/test_it.py::test_it[SET_01-loc_b-beta] dataset,loc_id SET_01 loc_b
PASSED
tests/005_conftest_fixt2/test_it.py::test_it[SET_02-loc_a-beta] dataset,loc_id SET_02 loc_a
PASSED
tests/005_conftest_fixt2/test_it.py::test_it[SET_02-loc_b-beta] dataset,loc_id SET_02 loc_b
PASSED
tests/005_conftest_fixt2/test_it.py::test_it[SET_01-loc_a-gama] dataset,loc_id SET_01 loc_a
PASSED
tests/005_conftest_fixt2/test_it.py::test_it[SET_01-loc_b-gama] dataset,loc_id SET_01 loc_b
PASSED
tests/005_conftest_fixt2/test_it.py::test_it[SET_02-loc_a-gama] dataset,loc_id SET_02 loc_a
PASSED
tests/005_conftest_fixt2/test_it.py::test_it[SET_02-loc_b-gama] dataset,loc_id SET_02 loc_b
PASSED

========================== 12 passed in 0.02 seconds ===========================
```

Instead of 4 tests as usually we see 12.

Closer look to test id values we see appearance of `-alfa`, `-beta` and `-gama`, what shall not
happen. In fact, the id `[SET_01-loc_a-alfa]` shows name of fixture `dataset` twice: once for
`SET_01` from our `test_it.py` what is fine, and then `alfa` from `conftest.py, what shall not
happen.

### 006_conftest_fixt2_fix: test file + `conftest.py` with dependent fixtures (fixed)

The last case is fixing the issue of duplicated tests again by using dummy fixture in our
`test_it.py` file:
```python
import pytest

DATASET_NAMES = ["SET_01", "SET_02"]
LOC_NAMES = ["loc_a", "loc_b"]


@pytest.fixture(scope="session")
def dataset():
    return "to-be-ignored"


def pytest_generate_tests(metafunc):
    dataset_names = DATASET_NAMES
    argnames = "dataset,loc_id"
    args_lst = []
    for dataset in dataset_names:
        for loc_id in LOC_NAMES:
            args_lst.append([dataset, loc_id])
    metafunc.parametrize(argnames, args_lst)


def test_it(dataset, loc_id):
    print("dataset,loc_id", dataset, loc_id)
```
Running the test suite we see all is fine:
```bash
$ py.test -sv tests/006_conftest_fixt2_fix/
============================= test session starts ==============================
platform linux -- Python 3.6.1, pytest-3.2.1, py-1.4.34, pluggy-0.4.0 -- /home/javl/.pyenv/versions/3.6.1/bin/python3.6
cachedir: .cache
rootdir: /home/javl/sandbox/generate_tests, inifile:
collecting ... collected 4 items

tests/006_conftest_fixt2_fix/test_it.py::test_it[SET_01-loc_a] dataset,loc_id SET_01 loc_a
PASSED
tests/006_conftest_fixt2_fix/test_it.py::test_it[SET_01-loc_b] dataset,loc_id SET_01 loc_b
PASSED
tests/006_conftest_fixt2_fix/test_it.py::test_it[SET_02-loc_a] dataset,loc_id SET_02 loc_a
PASSED
tests/006_conftest_fixt2_fix/test_it.py::test_it[SET_02-loc_b] dataset,loc_id SET_02 loc_b
PASSED

=========================== 4 passed in 0.01 seconds ===========================
```

## Summary

`pytest` excels in how one can author test cases with needed parameters and how these parameters can
be managed later on from multiple places:

- directly setting values at test function level
- parametrizing fixtures, which may be at the same file, in `conftest.py` in current directory or in
  any parent directory
- fixture values can be overriden on more specific levels when needed.

Provided examples exhibit two problems related to discovery of test cases, when
`pytest_generate_tests` is in place:

- "duplicate values" for value of a parameter, already provided by `pytest_generate_tests`
- collection of test cases collects more tests then needed using already used fixture for 2nd time.

### Duplicate values

As shown in `003_conftest_fixt1`, when `pytest_generate_tests` provided a value for test case
parameter and at the same time `conftest.py` provides a fixture with the same name, it wrongly
attempts to define a test case call also with the value from `conftest.py` fixture.

Expected behaviour is, that once a test function gets value for a parameter from
`pytest_generate_tests`, then further collection of values for this parameter shall stop.
Alternatively it shall resolve the duplication by giving the `pytest_generate_tests` parameter value
preference.

### Collection collects tests multiple times

As shown in `005_conftest_fixt2`, when `pytest_generate_tests` provides a value for a test case
parameter and at the same time in `conftest.py` there exist a fixture, which is dependent on another
one, it results in collecting the same test call (having the same combination of parameter values)
multiple times, this time it goes around `Duplicate values` by generating new test id using
parameter value from `conftest.py` fixture.

Expected behaviour is the same as described in "Duplicate values" above.
