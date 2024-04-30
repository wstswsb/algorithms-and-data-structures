import pytest

from structures.hashmap import HashMap


def test_create__without_args() -> None:
    # Act
    sut = HashMap()

    # Assert
    assert len(sut) == 0


def test__set_increments_len() -> None:
    # Arrange
    sut = HashMap()

    # Act
    sut.set("key", "value")

    # Assert
    assert len(sut) == 1


def test_hashmap__set_then_get() -> None:
    # Arrange
    sut = HashMap()

    # Act
    sut.set("key", "value")

    # Assert
    assert len(sut) == 1
    assert sut.get("key") == "value"


def test_set__new_value_with_same_key() -> None:
    # Arrange
    sut = HashMap()

    # Act
    sut.set("key", "value")
    sut.set("key", "another-value")
    result = sut.get("key")

    # Assert
    assert len(sut) == 1
    assert result == "another-value"


def test_set__collision_save_each_value() -> None:
    # Arrange
    sut = HashMap(max_key_hash=10)

    # Act
    assert all(sut.calculate_hash(key) == 2 for key in (2, 12, 22))
    sut.set(key=2, value="test-value-2")
    sut.set(key=12, value="test-value-12")
    sut.set(key=22, value="test-value-22")

    # Assert
    assert len(sut) == 3
    assert sut.get(2) == "test-value-2"
    assert sut.get(12) == "test-value-12"
    assert sut.get(22) == "test-value-22"


def test_set__invalid_key_type() -> None:
    # Arrange
    sut = HashMap()

    # Act\Assert
    with pytest.raises(TypeError):
        sut.set(key=[], value=object())


def test_get() -> None:
    # Arrange
    sut = HashMap()
    sut.set("key", "value")

    # Act
    result = sut.get("key")

    # Assert
    assert result == "value"


def test_get__non_existent_key() -> None:
    # Arrange
    sut = HashMap()

    # Act\Assert
    with pytest.raises(KeyError):
        sut.get("non-existent-key")
    assert len(sut) == 0


def test_get_non_existent_key_with_collision() -> None:
    # Arrange
    sut = HashMap(max_key_hash=10)
    sut.set(1, "test-value")

    # Act\Assert
    with pytest.raises(KeyError):
        sut.get(11)
    assert len(sut) == 1


def test_delete() -> None:
    # Arrange
    sut = HashMap()
    sut.set("key", "value")
    assert len(sut) == 1

    # Act
    sut.delete("key")

    # Assert
    assert len(sut) == 0
    with pytest.raises(KeyError):
        sut.get("key")


def test_delete__non_existent_key() -> None:
    # Arrange
    sut = HashMap()

    # Act\Assert
    with pytest.raises(KeyError):
        sut.delete("non-existent")


def test_delete_non_existent_key_with_collision() -> None:
    # Arrange
    sut = HashMap(max_key_hash=10)
    sut.set(1, "value-1")

    # Act
    with pytest.raises(KeyError):
        sut.delete(11)
