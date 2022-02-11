import pytest

from ..my_range import my_range


# Positive tests
def test_stop_positive():
    assert list(my_range(5)) == list(range(5))


def test_stop_negative():
    assert list(my_range(-5)) == list(range(-5))


def test_start_stop_positive():
    assert list(my_range(5, 10)) == list(range(5, 10))


def test_start_stop_negative():
    assert list(my_range(-5, -10)) == list(range(-5, -10))


def test_start_stop_step_positive():
    assert list(my_range(5, 10, 2)) == list(range(5, 10, 2))


def test_start_stop_step_negative():
    assert list(my_range(-10, -5, 3)) == list(range(-10, -5, 3))


def test_iterable():
    assert (iter(my_range(5)) is my_range(5)) == (iter(range(5)) is range(5))


# Negative tests
def test_unsupported_types():
    with pytest.raises(TypeError):
        my_range('abc')


def test_args_length():
    with pytest.raises(TypeError):
        my_range(0, 10, 3, 5)


def test_zero_step():
    with pytest.raises(ValueError):
        my_range(0, 5, 0)
