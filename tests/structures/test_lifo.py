import pytest

from structures.lifo import Lifo


def test_append() -> None:
    # Arrange
    sut = Lifo[int]()

    # Act
    sut.append(15)

    # Assert
    assert len(sut) == 1
    assert list(sut) == [15]


def test_pop() -> None:
    # Arrange
    sut = Lifo[int]()
    sut.append(12)
    sut.append(13)

    # Act
    result = sut.pop()
    # Assert
    assert result == 13


def test_pop__emtpy_items() -> None:
    # Arrange
    sut = Lifo[int]()

    # Act\Assert
    with pytest.raises(ValueError):
        sut.pop()
