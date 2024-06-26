import pytest

from algorithms.quick_sort import sort
from tests.algorithms.helpers import random_arrays


@pytest.mark.parametrize("items", random_arrays)
def test_sort(items: list[int]):
    assert sort(items) == sorted(items)
