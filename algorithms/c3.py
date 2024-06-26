from typing import Type

type TypesSequences = list[list[Type]]


def presented_in_tails(head: Type, types_sequences: TypesSequences) -> bool:
    for types_sequence in types_sequences:
        if head in types_sequence[1:]:
            return True
    return False


def _find_head(types_sequences: TypesSequences) -> Type:
    for types_sequence in types_sequences:
        head = types_sequence[0]
        if not presented_in_tails(head, types_sequences):
            return head
    raise TypeError("Cannot create MRO")


def _remove_head_from_starts(head: Type, types_sequences: TypesSequences) -> None:
    for types_sequence in types_sequences:
        if types_sequence[0] == head:
            del types_sequence[0]


def _remove_empty_sequences(types_sequences: TypesSequences) -> TypesSequences:
    return [sequence for sequence in types_sequences if sequence]


def _merge(types_sequences: TypesSequences) -> list[Type]:
    result: list[Type] = []
    while types_sequences := _remove_empty_sequences(types_sequences):
        head = _find_head(types_sequences)
        _remove_head_from_starts(head, types_sequences)
        result.append(head)
    return result


def c3(type_: Type) -> list:
    types_sequences = [
        [type_],
        *[c3(parent_type) for parent_type in type_.__bases__],
        list(type_.__bases__),
    ]
    return _merge(types_sequences)
