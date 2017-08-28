import pytest


DATASET_NAMES = ["alfa", "beta", "gama"]


@pytest.fixture(scope="session", params=DATASET_NAMES)
def dataset(request):
    return request.param
