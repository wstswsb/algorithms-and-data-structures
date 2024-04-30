import pytest

from structures.fifo import Fifo


def test_append_right():
    # Arrange
    sut = Fifo[int]()

    # Act
    sut.append_right(5)

    # Assert
    assert len(sut) == 1
    assert list(sut) == [5]


def test_append_right__many_times() -> None:
    # Arrange
    sut = Fifo()

    # Act
    sut.append_right(14)
    sut.append_right(15)
    sut.append_right(16)

    # Assert
    assert len(sut) == 3
    assert list(sut) == [14, 15, 16]


def test_pop_left() -> None:
    # Arrange
    sut = Fifo[int]()
    sut.append_right(1)
    sut.append_right(2)

    # Act
    result = sut.pop_left()

    # Assert
    assert result == 1
    assert len(sut) == 1
    assert list(sut) == [2]


def test_pop_left_empty_fifo() -> None:
    # Arrange
    sut = Fifo[int]()
    # Act\Assert
    with pytest.raises(ValueError):
        sut.pop_left()
