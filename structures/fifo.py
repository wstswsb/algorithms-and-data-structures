from collections.abc import Iterator

from structures.doubly_linked_list import DoublyLinkedList


class Fifo[T]:
    def __init__(self):
        self.items = DoublyLinkedList()

    def __len__(self) -> int:
        return len(self.items)

    def __iter__(self) -> Iterator[T]:
        return iter(self.items)

    def append_right(self, value: T) -> None:
        self.items.append(value)

    def pop_left(self) -> T:
        if len(self) == 0:
            raise ValueError("Fifo is empty")
        item = self.items.get(0)
        self.items.delete(0)
        return item
