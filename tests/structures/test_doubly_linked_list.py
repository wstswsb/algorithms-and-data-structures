import os

import pytest
from line_profiler import profile

from structures.doubly_linked_list import DoublyLinkedList, Node


def test_node__repr() -> None:
    # Arrange
    sut = Node("test")

    # Act
    result = repr(sut)

    # Assert
    assert result == "Node(test)"


def test_init() -> None:
    # Act
    sut = DoublyLinkedList()

    # Assert
    assert len(sut) == 0
    assert sut.head is None
    assert sut.tail is None


def test_append__first() -> None:
    # Arrange
    sut = DoublyLinkedList[int]()

    # Act
    sut.append(13)

    # Assert
    assert len(sut) == 1

    assert isinstance(sut.head, Node)
    assert sut.head.data == 13
    assert sut.head.next_node is None
    assert sut.head.prev_node is None

    assert sut.tail is sut.head


def test_append__many() -> None:
    # Arrange
    sut = DoublyLinkedList[str]()

    # Act
    sut.append("a")
    sut.append("b")
    sut.append("c")

    # Assert
    assert len(sut) == 3

    head = sut.head
    assert isinstance(head, Node)
    assert head.data == "a"
    assert head.prev_node is None

    second_node = head.next_node
    assert isinstance(second_node, Node)
    assert second_node.data == "b"
    assert second_node.prev_node is head

    third_node = second_node.next_node
    assert isinstance(third_node, Node)
    assert third_node.data == "c"
    assert third_node.next_node is None
    assert third_node.prev_node is second_node

    assert third_node is sut.tail


def test__from_iterable() -> None:
    # Act
    sut = DoublyLinkedList.from_iterable("ab")

    # Assert
    assert len(sut) == 2

    head = sut.head
    assert isinstance(head, Node)
    assert head.data == "a"
    assert head.prev_node is None

    second_node = head.next_node
    assert isinstance(second_node, Node)
    assert second_node.data == "b"
    assert second_node.prev_node is head
    assert second_node.next_node is None

    assert sut.tail is second_node


def test_prepend__empty() -> None:
    # Arrange
    sut = DoublyLinkedList[int]()

    # Act
    sut.prepend(12)

    # Assert
    assert len(sut) == 1

    assert isinstance(sut.head, Node)
    assert sut.head.data == 12
    assert sut.head.prev_node is None
    assert sut.head.next_node is None

    assert sut.head is sut.tail


def test_prepend__not_empty() -> None:
    # Arrange
    sut = DoublyLinkedList.from_iterable("bcd")

    # Act
    sut.prepend("a")

    # Assert
    assert len(sut) == 4

    assert sut.get(0) == "a"
    assert sut.get(1) == "b"
    assert sut.get(2) == "c"
    assert sut.get(3) == "d"

    assert isinstance(sut.head, Node)
    assert sut.head.data == "a"
    assert sut.head.prev_node is None

    second_node = sut.head.next_node
    assert isinstance(second_node, Node)
    assert second_node.data == "b"
    assert second_node.prev_node is sut.head

    third_node = second_node.next_node
    assert isinstance(third_node, Node)
    assert third_node.data == "c"
    assert third_node.prev_node is second_node

    fourth_node = third_node.next_node
    assert isinstance(fourth_node, Node)
    assert fourth_node.data == "d"
    assert fourth_node.prev_node is third_node
    assert fourth_node.next_node is None

    assert fourth_node is sut.tail


def test_get__empty_list() -> None:
    # Arrange
    sut = DoublyLinkedList()

    # Act\Assert
    with pytest.raises(IndexError):
        sut.get(1)


def test_get__not_empty_out_of_range() -> None:
    # Arrange
    sut = DoublyLinkedList[int]()
    sut.append(1)

    # Act\Assert
    with pytest.raises(IndexError):
        sut.get(1)


def test_get() -> None:
    # Arrange
    sut = DoublyLinkedList[int]()
    sut.append(1)
    sut.append(2)
    sut.append(3)

    # Act
    result = sut.get(2)

    # Assert
    assert len(sut) == 3
    assert result == 3


def test_get__negative_index_error() -> None:
    # Arrange
    sut = DoublyLinkedList[int]()
    sut.append(1)

    # Act\Assert
    with pytest.raises(IndexError):
        sut.get(-1)


def test_update__index_error() -> None:
    # Arrange
    sut = DoublyLinkedList[int]()
    sut.append(1)

    # Act\Assert
    with pytest.raises(IndexError):
        sut.update(index=1, value=5)


def test_update_valid() -> None:
    # Arrange
    sut = DoublyLinkedList[int]()
    sut.append(1)
    sut.append(2)
    sut.append(3)

    # Act
    sut.update(index=1, value=55)

    # Assert
    assert len(sut) == 3

    assert sut.get(0) == 1
    assert sut.get(1) == 55
    assert sut.get(2) == 3


def test_delete__only_head() -> None:
    # Arrange
    sut = DoublyLinkedList[int]()
    sut.append(1)

    # Act
    sut.delete(0)

    # Assert
    assert len(sut) == 0

    assert sut.head is None
    assert sut.tail is None


def test_delete__last_item() -> None:
    # Arrange
    sut = DoublyLinkedList.from_iterable("abc")

    # Act
    sut.delete(2)

    # Assert
    assert len(sut) == 2

    assert sut.get(0) == "a"
    assert sut.get(1) == "b"
    with pytest.raises(IndexError):
        sut.get(2)


def test_delete__has_previous_and_next() -> None:
    # Arrange
    sut = DoublyLinkedList[int]()
    sut.append(1)
    sut.append(2)
    sut.append(3)

    # Act
    sut.delete(1)

    # Assert
    assert len(sut) == 2

    assert sut.get(0) == 1
    assert sut.get(1) == 3
    with pytest.raises(IndexError):
        sut.get(2)


def test_delete__head() -> None:
    # Arrange
    sut = DoublyLinkedList.from_iterable("abc")

    # Act
    sut.delete(0)

    # Assert
    assert len(sut) == 2

    assert sut.head.data == "b"
    assert sut.head.prev_node is None
    assert sut.head.next_node is sut.tail

    assert sut.tail.data == "c"
    assert sut.tail.prev_node is sut.head
    assert sut.tail.next_node is None


def test_delete__head_and_tail_list():
    # Arrange
    sut = DoublyLinkedList.from_iterable("ab")

    # Act
    sut.delete(0)

    # Assert
    assert len(sut) == 1
    assert sut.head.data == "b"
    assert sut.head is sut.tail
    assert sut.head.next_node is sut.head.prev_node is None


def test_delete__empty() -> None:
    # Arrange
    sut = DoublyLinkedList()

    # Act\Assert
    with pytest.raises(IndexError):
        sut.delete(0)


def test_iterator__empty() -> None:
    # Arrange
    sut = DoublyLinkedList()

    # Act
    result = [item for item in sut]

    # Assert
    assert result == []


def test_iterator__only_head() -> None:
    # Arrange
    sut = DoublyLinkedList[int]()
    sut.append(12)

    # Act
    result = [item for item in sut]

    # Assert
    assert result == [12]


def test_iterator__three_values() -> None:
    # Arrange
    sut = DoublyLinkedList[int]()
    sut.append(1)
    sut.append(2)
    sut.append(3)

    # Act
    result = [item for item in sut]

    # Assert
    assert result == [1, 2, 3]


@pytest.mark.skipif(os.getenv("LINE_PROFILE") != "1", reason="profile mode disabled")
@profile
def test_native_list_and_custom_creation_performance():
    for _ in range(1_000):
        list(range(10_000))
        DoublyLinkedList.from_iterable(range(10_000))
