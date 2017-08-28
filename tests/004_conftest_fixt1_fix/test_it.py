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
