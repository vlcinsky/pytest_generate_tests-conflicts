import pytest

DATASET_NAMES = ["SET_01", "SET_02"]
LOC_NAMES = ["loc_a", "loc_b"]


PARAMS = [(set_name, loc_id)
          for set_name in DATASET_NAMES
          for loc_id in LOC_NAMES]


@pytest.mark.parametrize("dataset,loc_id", PARAMS)
def test_it(dataset, loc_id):
    print("dataset, loc_id", dataset, loc_id)
