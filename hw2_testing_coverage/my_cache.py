from functools import wraps
from typing import Callable


class Cache:
    '''
    Decorator for caching.

    If `use_cache` is True function returns cached result only
    when function called using the same positional/keyword arguments
    distribution.
    For instance: if we firstly invoke `foo(1, 2)`
    and then `foo(1, b=2)` we will compute function once again
    because `b` is keyword argument now.

    It also depends on `__repr__` method implementation of given arguments.
    '''
    def __init__(self, use_cache: bool = True) -> None:
        self.use_cache = use_cache
        self.cache = dict()

    def __call__(self, func: Callable):
        @wraps(func)
        def inner(*args, **kwargs):
            key = '_'.join(map(repr, args)) + '_'
            key += '_'.join(map(repr, sorted(kwargs.items())))

            if (not self.use_cache) or (key not in self.cache):
                self.cache[key] = func(*args, **kwargs)

            return self.cache[key]

        return inner
