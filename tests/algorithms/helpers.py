import random

random_arrays: list[list[int]] = [
    [random.randint(1, 1000) for i in range(1, 1000)]
    for _ in range(10)
]  # fmt: skip
