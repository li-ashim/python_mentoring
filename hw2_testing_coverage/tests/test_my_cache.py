from typing import Callable

from ..my_cache import Cache


# Utils
def _count_calls(func: Callable):
    def inner(*args, **kwargs):
        inner._counter += 1
        func(*args, **kwargs)
    inner._counter = 0
    return inner


def _get_initial_and_cached_funcs(func: Callable, use_cache: bool):
    '''Returns initial function with counter and cached function'''
    initial_func = _count_calls(func)
    cached_func = Cache(use_cache)(initial_func)
    return initial_func, cached_func


# Tests
def test_cache_only_positional_args():
    def foo(a, b, /):
        return a, b

    initial_foo, cached_foo = _get_initial_and_cached_funcs(foo, True)

    n = 3
    for i in range(n):
        cached_foo(1, 2)

    assert initial_foo._counter == 1


def test_no_cache_only_positional_args():
    def foo(a, b, /):
        return a, b

    initial_foo, cached_foo = _get_initial_and_cached_funcs(foo, False)

    n = 3
    for i in range(n):
        cached_foo(1, 2)

    assert initial_foo._counter == n


def test_cache_only_keyword_args():
    def foo(*, a, b):
        return a, b

    initial_foo, cached_foo = _get_initial_and_cached_funcs(foo, True)

    n = 3
    for i in range(n):
        cached_foo(a=1, b=2)

    assert initial_foo._counter == 1


def test_cache_only_keyword_args_diff_order():
    def foo(*, a, b, c):
        return a, b, c

    initial_foo, cached_foo = _get_initial_and_cached_funcs(foo, True)

    cached_foo(a=1, b=2, c=3)
    cached_foo(b=2, c=3, a=1)
    cached_foo(c=3, a=1, b=2)

    assert initial_foo._counter == 1


def test_no_cache_only_keyword_args_diff_order():
    def foo(*, a, b, c):
        return a, b, c

    initial_foo, cached_foo = _get_initial_and_cached_funcs(foo, False)

    cached_foo(a=1, b=2, c=3)
    cached_foo(b=2, c=3, a=1)
    cached_foo(c=3, a=1, b=2)

    assert initial_foo._counter == 3


def test_cache_mixed_args():
    def foo(a, b, c=3):
        return a, b, c

    initial_foo, cached_foo = _get_initial_and_cached_funcs(foo, True)

    n = 3
    for i in range(n):
        cached_foo(1, 2, c=4)

    assert initial_foo._counter == 1
