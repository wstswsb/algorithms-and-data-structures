from collections.abc import Iterator

from structures.doubly_linked_list import DoublyLinkedList


class Lifo[T]:
    def __init__(self):
        self.items = DoublyLinkedList[T]()

    def __len__(self) -> int:
        return len(self.items)

    def __iter__(self) -> Iterator[T]:
        return iter(self.items)

    def append(self, value: T) -> None:
        self.items.append(value)

    def pop(self) -> T:
        if len(self) == 0:
            raise ValueError("Lifo is empty")
        last_item_index = len(self) - 1
        return self.items.get(last_item_index)
