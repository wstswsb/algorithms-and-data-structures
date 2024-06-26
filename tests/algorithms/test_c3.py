from typing import Type

import pytest

from algorithms.c3 import c3

# fmt: off
O = object # noqa
class F(O): pass # noqa
class E(O): pass # noqa
class D(O): pass # noqa
class C(D, F): pass # noqa
class B(D, E): pass # noqa
class A(B, C): pass # noqa
# fmt: on


@pytest.mark.parametrize(
    "base, expected_result",
    [
        (O, [O]),
        (D, [D, O]),
        (E, [E, O]),
        (F, [F, O]),
        (B, [B, D, E, O]),
        (C, [C, D, F, O]),
        (A, [A, B, C, D, E, F, O]),
    ],
)
def test_c3(base: Type, expected_result: list[Type]) -> None:
    assert c3(base) == expected_result
