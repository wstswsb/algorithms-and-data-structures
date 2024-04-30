from functools import reduce
from operator import xor
from typing import Any, NamedTuple, Final

from structures.doubly_linked_list import DoublyLinkedList

type HashmapItems = DoublyLinkedList[HashmapItems]
type Key = int | str


class _HashMapItem(NamedTuple):
    key: Key
    value: Any


class HashMap:
    _NOT_FOUND_INDEX: Final[int] = -1

    def __init__(self, max_key_hash: int = 100):
        self._length = 0
        self._max_key_hash: Final[int] = max_key_hash
        self._store: list[DoublyLinkedList | None] = [None for _ in range(max_key_hash)]

    def __repr__(self) -> str:
        return f"HashMap(len={self._length})"

    def __len__(self) -> int:
        return self._length

    def set(self, key: Key, value: Any) -> None:
        key_hash = self.calculate_hash(key)
        hashmap_items = self._get_or_create_hashmap_items(key_hash)
        key_index = self._find_key_index(key, hashmap_items)
        self._insert_hashmap_item(_HashMapItem(key, value), key_index, hashmap_items)

    def get(self, key: Key) -> Any:
        key_hash = self.calculate_hash(key)
        hashmap_items = self._get_or_raise_hashmap_items(key_hash)
        return self._find_or_raise_value(key, hashmap_items)

    def delete(self, key: Key) -> None:
        key_hash = self.calculate_hash(key)
        hashmap_items = self._get_or_raise_hashmap_items(key_hash)
        self._delete_or_raise_key(key, hashmap_items)
        self._actualize_store(key_hash, hashmap_items)

    def _delete_or_raise_key(self, key: Key, hashmap_items: HashmapItems) -> None:
        key_index = self._find_key_index(key, hashmap_items)
        if key_index == self._NOT_FOUND_INDEX:
            raise KeyError()
        hashmap_items.delete(key_index)
        self._length -= 1

    def calculate_hash(self, key: int | str) -> int:
        match key:
            case int():
                return key % self._max_key_hash
            case str():
                return reduce(xor, key.encode()) % self._max_key_hash
            case _:
                raise TypeError("key must be int or str")

    def _actualize_store(self, key_hash: int, hashmap_items: HashmapItems) -> None:
        if len(hashmap_items) == 0:
            self._store[key_hash] = None

    def _find_or_raise_value(self, key: Key, hashmap_items: HashmapItems) -> Any:
        for hashmap_item in hashmap_items:
            if hashmap_item.key != key:
                continue
            return hashmap_item.value
        raise KeyError()

    def _get_or_raise_hashmap_items(self, key_hash: int) -> HashmapItems:
        hashmap_items = self._store[key_hash]
        if hashmap_items is None:
            raise KeyError()
        return hashmap_items

    def _get_or_create_hashmap_items(self, key_hash: int) -> HashmapItems:
        hashmap_items = self._store[key_hash]
        if hashmap_items is None:
            hashmap_items = DoublyLinkedList[_HashMapItem]()
            self._store[key_hash] = hashmap_items
        return hashmap_items

    def _insert_hashmap_item(
        self,
        item: _HashMapItem,
        index: int,
        collection: HashmapItems,
    ):
        if index != self._NOT_FOUND_INDEX:
            collection.update(index, item)
        else:
            collection.append(item)
            self._length += 1

    def _find_key_index(
        self,
        key: int | str,
        hashmap_items: DoublyLinkedList[_HashMapItem],
    ) -> int:
        key_index = self._NOT_FOUND_INDEX
        for index, hashmap_item in enumerate(hashmap_items):
            if hashmap_item.key != key:
                continue
            return index
        return key_index
