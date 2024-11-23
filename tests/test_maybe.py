import pytest

from fp_py.Maybe import Maybe, Nothing, Some
from assertpy import assert_that

from fp_py.types import typed_lambda



def test_maybe_nothing():
    v = Nothing()
    assert_that(v.is_none()).is_true()
    assert_that(v.is_some()).is_false()
    
def test_maybe_some():
    v = Some(42)
    assert_that(v.is_none()).is_false()
    assert_that(v.is_some()).is_true()
    assert_that(v.unwrap()).is_equal_to(42)

def test_maybe_none_match():
    v = Nothing()
    res = v.match(lambda:"Nothing", lambda x: x+2)
    assert_that(res).is_equal_to("Nothing")
    
def test_maybe_some_match():
    v = Some('Test')
    res = v.match(lambda:"Nothing", lambda x: x+" Test")
    assert_that(res).is_equal_to("Test Test")

def test_maybe_bind():
    v = Some('Test')
    f: typed_lambda[str] = lambda x: len(x)
    s: typed_lambda[int] = lambda x: x+2
    m: typed_lambda[int] = lambda c: None
    assert_that(v.bind(f).bind(s).unwrap()).is_equal_to(6)
    assert_that(v.bind(f).bind(m).is_none()).is_true()

def test_maybe_wrap():
    assert_that(Maybe[int].wrap(43).is_some()).is_true()
    assert_that(Maybe[int].wrap(None).is_some()).is_false()
    assert_that(Maybe[int].wrap(None).is_none()).is_true()