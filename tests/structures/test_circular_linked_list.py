import os

import pytest
from line_profiler import profile

from structures.circular_linked_list import CircularList, Node


def test_node__repr() -> None:
    # Arrange
    sut = Node("test")

    # Act
    result = repr(sut)

    # Assert
    assert result == "Node(test)"


def test_init() -> None:
    # Act
    result = CircularList()

    # Assert
    assert result.head is None
    assert result.tail is None


def test_append__first() -> None:
    # Arrange
    sut = CircularList[int]()

    # Act
    sut.append(13)

    # Assert
    assert isinstance(sut.head, Node)
    assert sut.head.data == 13
    assert sut.head.next_node is sut.head

    assert sut.tail is sut.head


def test_append__many() -> None:
    # Arrange
    sut = CircularList[str]()

    # Act
    sut.append("a")
    sut.append("b")
    sut.append("c")

    # Assert
    head = sut.head
    assert isinstance(head, Node)
    assert head.data == "a"

    second_node = head.next_node
    assert isinstance(second_node, Node)
    assert second_node.data == "b"

    third_node = second_node.next_node
    assert isinstance(third_node, Node)
    assert third_node.data == "c"
    assert third_node.next_node is head

    assert third_node is sut.tail


def test__from_iterable() -> None:
    # Arrange
    iterable = [1, 2]

    # Act
    sut = CircularList.from_iterable(iterable)

    # Assert
    head = sut.head
    assert isinstance(head, Node)
    assert head.data == 1

    second_node = head.next_node
    assert isinstance(second_node, Node)
    assert second_node.data == 2

    assert sut.tail is second_node


def test_prepend__empty() -> None:
    # Arrange
    sut = CircularList[int]()

    # Act
    sut.prepend(12)

    # Assert
    assert isinstance(sut.head, Node)
    assert sut.head is sut.tail
    assert sut.head.data == 12


def test_prepend__not_empty() -> None:
    # Arrange
    sut = CircularList.from_iterable("bcd")

    # Act
    sut.prepend("a")

    # Assert
    assert sut.get(0) == "a"
    assert sut.get(1) == "b"
    assert sut.get(2) == "c"
    assert sut.get(3) == "d"

    assert isinstance(sut.head, Node)
    assert sut.head.data == "a"

    assert isinstance(sut.tail, Node)
    assert sut.tail.data == "d"


def test_get__empty_list() -> None:
    # Arrange
    sut = CircularList()

    # Act\Assert
    with pytest.raises(IndexError):
        sut.get(1)


def test_get() -> None:
    # Arrange
    sut = CircularList[int]()
    sut.append(1)
    sut.append(2)
    sut.append(3)

    # Act
    result = sut.get(2)

    # Assert
    assert result == 3


def test_get__negative_index_error() -> None:
    # Arrange
    sut = CircularList[int]()
    sut.append(1)

    # Act\Assert
    with pytest.raises(IndexError):
        sut.get(-1)


def test_update__circular() -> None:
    # Arrange
    sut = CircularList.from_iterable("abc")

    # Act
    sut.update(index=4, value="upd")

    # Assert
    assert sut.get(0) == "a"
    assert sut.get(1) == "upd"
    assert sut.get(2) == "c"


def test_update() -> None:
    # Arrange
    sut = CircularList.from_iterable("abc")

    # Act
    sut.update(index=2, value="upd")

    # Assert
    assert sut.get(0) == "a"
    assert sut.get(1) == "b"
    assert sut.get(2) == "upd"
    assert sut.tail.data == sut.get(2)
    assert sut.tail.next_node is sut.head


def test_update__tail():
    pass


def test_delete__only_head() -> None:
    # Arrange
    sut = CircularList.from_iterable("a")

    # Act
    sut.delete(0)

    # Assert
    assert sut.head is None
    assert sut.tail is None


def test_delete__last_item() -> None:
    # Arrange
    sut = CircularList.from_iterable("abc")
    start_len = len(sut)

    # Act
    sut.delete(2)

    # Assert
    assert sut.get(0) == "a"
    assert sut.get(1) == "b"

    assert sut.get(2) is sut.get(0)
    assert sut.tail.next_node is sut.head
    assert len(sut) == start_len - 1


def test_delete__has_previous_and_next() -> None:
    # Arrange
    sut = CircularList.from_iterable("abc")
    start_len = len(sut)

    # Act
    sut.delete(1)

    # Assert
    assert sut.get(0) == "a"
    assert sut.get(1) == "c"

    assert sut.get(2) is sut.get(0)
    assert sut.tail.next_node is sut.head
    assert len(sut) == start_len - 1


def test_delete__head_not_emtpy() -> None:
    # Arrange
    sut = CircularList.from_iterable("abc")
    start_len = len(sut)

    # Act
    sut.delete(0)

    # Assert
    assert sut.get(0) == "b"
    assert sut.get(1) == "c"

    assert sut.get(2) is sut.get(0)
    assert sut.tail.next_node is sut.head
    assert len(sut) == start_len - 1


def test_delete__head_and_tail_list():
    # Arrange
    sut = CircularList.from_iterable("ab")

    # Act
    sut.delete(0)

    # Assert
    assert len(sut) == 1
    assert sut.head.data == "b"
    assert sut.head is sut.tail
    assert sut.tail.next_node is sut.head


def test_delete__empty() -> None:
    # Arrange
    sut = CircularList()

    # Act\Assert
    with pytest.raises(IndexError):
        sut.delete(0)


def test_iterator__empty() -> None:
    # Arrange
    sut = CircularList()

    # Act
    result = [item for item in sut]

    # Assert
    assert result == []


def test_iterator__only_head() -> None:
    # Arrange
    sut = CircularList[int]()
    sut.append(12)

    # Act
    result = [item for item in sut]

    # Assert
    assert result == [12]


def test_iterator__three_values() -> None:
    # Arrange
    sut = CircularList.from_iterable(range(1, 4))

    # Act
    result = [item for item in sut]

    # Assert
    assert result == [1, 2, 3]


@pytest.mark.skipif(os.getenv("LINE_PROFILE") != "1", reason="profile mode disabled")
@profile
def test_native_list_and_custom_creation_performance():
    for _ in range(1_000):
        list(range(10_000))
        CircularList.from_iterable(range(10_000))
