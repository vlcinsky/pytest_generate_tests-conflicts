import pytest


DATASET_NAMES = ["alfa", "beta", "gama"]


@pytest.fixture(scope="module", params=DATASET_NAMES)
def dataset_name(request):
    return request.param


@pytest.fixture(scope="session")
def dataset(dataset_name):
    return dataset_name
