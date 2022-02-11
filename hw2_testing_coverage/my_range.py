from typing import Iterator, Sequence


class my_range:
    '''Simulates behavior of built-in function `range`'''
    def __init__(self, *args: Sequence[int]) -> None:
        if len(args) > 3:
            raise TypeError('my_range expected at most 3 arguments, '
                            f'got {len(args)}')
        for arg in args:
            if not isinstance(arg, int):
                raise TypeError(f'{arg.__class__.__name__} object '
                                'cannot be interpreted as an integer')
        self.start = 0
        self.step = 1
        if len(args) == 1:
            [self.stop] = args
        elif len(args) == 2:
            self.start, self.stop = args
        elif len(args) == 3:
            self.start, self.stop, self.step = args
            if self.step == 0:
                raise ValueError('my_range() arg 3 must not be zero')

    def __iter__(self) -> Iterator:
        return MyRangeIter(self.start, self.stop, self.step)


class MyRangeIter:
    def __init__(self, start: int, stop: int, step: int) -> None:
        self.start = start
        self.stop = stop
        self.step = step
        self.val = self.start

    def __next__(self) -> int:
        if ((self.step > 0 and self.val >= self.stop) or
                (self.step < 0 and self.val <= self.stop)):
            raise StopIteration
        value = self.val
        self.val += self.step
        return value
