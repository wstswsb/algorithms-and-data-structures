def merge(left: list[int], right: list[int]) -> list[int]:
    result: list[int] = []

    index_left = 0
    index_right = 0
    while index_left < len(left) and index_right < len(right):
        left_item = left[index_left]
        right_item = right[index_right]

        if left_item <= right_item:
            result.append(left_item)
            index_left += 1
        else:
            result.append(right_item)
            index_right += 1

    missed_items = left[index_left:] + right[index_right:]
    result.extend(missed_items)
    return result


def sort(items: list[int]) -> list[int]:
    border = len(items) // 2
    left = items[:border]
    right = items[border:]

    if len(left) > 1:
        left = sort(left)
    if len(right) > 1:
        right = sort(right)
    return merge(left, right)
