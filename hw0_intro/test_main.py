import pytest

from hw0_intro.main import multiply


def test_multiply_positive_numbers():
    assert multiply(1, 2) == 2


def test_multiply_zero():
    assert multiply(1, 0) == 0


def test_multiply_type_error():
    with pytest.raises(TypeError):
        multiply('a', 'b')
