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
