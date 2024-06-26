import random


def sort(items: list[int]):
    if len(items) < 2:
        return items
    pivot = items[random.randint(0, len(items) - 1)]
    lower_than_pivot: list[int] = []
    equal_pivot: list[int] = []
    higher_than_pivot: list[int] = []
    for item in items:
        if item < pivot:
            lower_than_pivot.append(item)
        elif item == pivot:
            equal_pivot.append(item)
        else:
            higher_than_pivot.append(item)
    return sort(lower_than_pivot) + equal_pivot + sort(higher_than_pivot)
