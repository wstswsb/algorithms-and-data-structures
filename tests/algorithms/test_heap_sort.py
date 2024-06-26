import pytest

from algorithms.heap_sort import sort
from tests.algorithms.helpers import random_arrays


@pytest.mark.parametrize("items", random_arrays)
def test_sort(items: list[int]):
    result = sort(items)
    assert result is items
    assert result == sorted(items)
