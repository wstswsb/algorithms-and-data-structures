from collections.abc import Iterable
from typing import Self


class Node[T]:
    __slots__ = ("data", "next_node")

    def __init__(self, data: T):
        self.data = data
        self.next_node: Self | None = None

    def __repr__(self) -> str:
        return f"Node({self.data})"


class CircularList[T]:
    def __init__(self):
        self.head: Node[T] | None = None
        self.tail: Node[T] | None = None
        self._length = 0

    def __iter__(self):
        current = self.head
        if current is None:
            return
        while True:
            yield current.data
            current = current.next_node
            if current is self.head:
                break

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
        circular_list = CircularList[T]()
        for item in iterable:
            circular_list.append(item)
        return circular_list

    def get(self, index: int) -> T:
        return self._get_node(index).data

    def append(self, data: T) -> None:
        match self.head, self.tail:
            case None, None:
                self.head = self.tail = Node(data)
                self.tail.next_node = self.head
                self._increment_length()
            case _, Node():
                self.tail.next_node = Node(data)
                self.tail.next_node.next_node = self.head
                self.tail = self.tail.next_node
                self._increment_length()

    def prepend(self, data: T) -> None:
        match self.head:
            case None:
                self.head = self.tail = Node(data)
                self.tail.next_node = self.head
                self._increment_length()
            case Node():
                new_head = Node(data)
                new_head.next_node = self.head
                self.tail.next_node = new_head
                self.head = new_head
                self._increment_length()

    def update(self, index: int, value: T) -> None:
        node = self._get_node(index)
        node.data = value

    def delete(self, index: int) -> None:
        if self._length == 0:
            raise IndexError("delete from emtpy list")
        match index:
            case 0:
                self._delete_head()
            case int():
                self._delete_not_head(index)

    def _delete_head(self):
        if self.head is self.tail:
            self.head = self.tail = None
        else:
            self.head = self.head.next_node
            self.tail.next_node = self.head
        self._decrement_length()

    def _delete_not_head(self, index):
        previous_node = self._get_node(index - 1)
        current_node = previous_node.next_node
        previous_node.next_node = current_node.next_node
        if current_node is self.tail:
            self.tail = previous_node
        self._decrement_length()

    def _get_node(self, index: int) -> Node[T]:
        if index < 0:
            raise IndexError("Index must be positive integer")
        if self._length == 0:
            raise IndexError("get item from empty list")
        if self._length > 0:
            index = index % self._length
        if index == self._length - 1:
            return self.tail

        current_node = self.head
        for _ in range(index):
            current_node = current_node.next_node
        return current_node
