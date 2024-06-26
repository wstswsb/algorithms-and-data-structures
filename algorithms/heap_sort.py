def heapify(items: list[int], last_item_index: int, root_index: int) -> None:
    # max in root
    largest_index = root_index
    left_child_index = 2 * root_index + 1
    right_child_index = 2 * root_index + 2

    if left_child_index < last_item_index and items[largest_index] < items[left_child_index]:  # fmt: skip
        largest_index = left_child_index

    if right_child_index < last_item_index and items[largest_index] < items[right_child_index]:  # fmt: skip
        largest_index = right_child_index

    if largest_index != root_index:
        items[root_index], items[largest_index] = items[largest_index], items[root_index]  # fmt: skip
        heapify(items, last_item_index, root_index=largest_index)


def convert_to_max_heap(items: list[int]) -> None:
    first_root_index = (len(items) // 2) - 1
    for root_index in range(first_root_index, -1, -1):
        heapify(items, last_item_index=len(items), root_index=root_index)


def sort_max_heap(items_heap: list[int]) -> None:
    last_item_index = len(items_heap) - 1
    for index in range(last_item_index, 0, -1):
        # после этого шага про items_heap нельзя сказать, что она max_heap
        items_heap[index], items_heap[0] = items_heap[0], items_heap[index]
        # восстанавливаем свойство max_heap для items_heap
        heapify(items_heap, last_item_index=index, root_index=0)


def sort(items: list[int]) -> list[int]:
    convert_to_max_heap(items)
    sort_max_heap(items)
    return items
