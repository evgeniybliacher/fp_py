from typing import TypeVar
import pytest
from assertpy import assert_that
from fp_py.types import typed_lambda, untyped_lambda


T = TypeVar('T')
R = TypeVar('R')
Func = TypeVar('F', bound = typed_lambda[T])
Action = TypeVar('Action', bound=untyped_lambda)

def test_typed_int():
    val = typed_lambda[int, int](lambda x: x+2)
    assert_that(val(2)).is_equal_to(4)

def test_typed_string():
    val = typed_lambda[str, int](lambda s: len(s))
    assert_that(val("Hello!!!")).is_equal_to(8)

def test_untyped_string():
    val = untyped_lambda(lambda : "42")
    assert_that(val()).is_equal_to("42")

def test_typed_type():
    val : Func[int] = typed_lambda[int,int](lambda x: x + 2)
    def d(f : Func, i: T)-> int:
        return f(i)
    assert_that(d(val, 5)).is_equal_to(7)

def test_untyped_type():
    val : Action = untyped_lambda(lambda : 47)
    def d(f : Action)-> int:
        return f()
    assert_that(d(val)).is_equal_to(47)