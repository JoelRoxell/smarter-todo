from typing import Callable, TypeVar
import functools

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')


def combine(f: Callable[[B], C], g: Callable[[A], B]) -> Callable[[A], C]:
    def h(x: A) -> C:
        return f(g(x))
    return h


def compose(*fns: Callable) -> Callable:
    return functools.reduce(combine, fns)
