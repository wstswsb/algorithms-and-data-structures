from collections.abc import Iterable
from typing import Self


class Node[T]:
    __slots__ = ("data", "next_node", "prev_node")

    def __init__(self, data: T):
        self.data = data
        self.next_node: Self | None = None
        self.prev_node: Self | None = None

    def __repr__(self) -> str:
        return f"Node({self.data})"


class DoublyLinkedList[T]:
    def __init__(self):
        self.head: Node[T] | None = None
        self.tail: Node[T] | None = None
        self._length = 0

    def __iter__(self):
        current = self.head
        while current is not None:
            yield current.data
            current = current.next_node

    def __len__(self) -> int:
        return self._length

    def _decrement_length(self):
        if self._length == 0:
            raise RuntimeError("invalid operation, length cannot be less then 0")
        self._length -= 1

    def _increment_length(self):
        self._length += 1

    @staticmethod
    def from_iterable(iterable: Iterable[T]):  # noqa
        linked_list = DoublyLinkedList[T]()
        for item in iterable:
            linked_list.append(item)
        return linked_list

    def get(self, index: int) -> T:
        return self._get_node(index).data

    def append(self, data: T) -> None:
        match self.head, self.tail:
            case None, None:
                self.head = Node(data)
                self.tail = self.head
                self._increment_length()
            case _, Node():
                self.tail.next_node = Node(data)
                self.tail.next_node.prev_node = self.tail
                self.tail = self.tail.next_node
                self._increment_length()

    def prepend(self, data: T) -> None:
        match self.head:
            case None:
                self.head = Node(data)
                self.tail = self.head
                self._increment_length()
            case Node():
                self.head.prev_node = Node(data)
                self.head.prev_node.next_node = self.head
                self.head = self.head.prev_node
                self._increment_length()

    def update(self, index: int, value: T) -> None:
        node = self._get_node(index)
        node.data = value

    def delete(self, index: int) -> None:
        if self._length == 0:
            raise IndexError("delete from empty list")
        match index:
            case 0:
                self._delete_head()
            case int():
                self._delete_not_head(index)

    def _delete_head(self):
        if self.head is self.tail:
            self.head = self.tail = None
        elif self.head.next_node is self.tail:
            self.head = self.tail
            self.head.prev_node = self.head.next_node = None
        else:
            self.head = self.head.next_node
            self.head.prev_node = None
        self._decrement_length()

    def _delete_not_head(self, index):
        current_node = self._get_node(index)
        current_node.prev_node.next_node = None
        if current_node is self.tail:
            self.tail = current_node.prev_node
        self._decrement_length()

    def _get_node(self, index: int) -> Node[T]:
        if index < 0:
            raise IndexError("Index must be positive integer")
        if index >= self._length:
            raise IndexError("Index out of range")
        if index == self._length - 1:
            return self.tail

        current_node = self.head
        for _ in range(index):
            current_node = current_node.next_node
        return current_node
