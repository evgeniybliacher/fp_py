import pytest

from fp_py.Either import Left, Right
from fp_py.Maybe import Just, Maybe, Nothing
from assertpy import assert_that,fail


#pure = Just.pure
#unit = Just.unit

@pytest.mark.either
def test_either_functor():
    assert_that((Left(2)+Right(3)).is_left()).is_true()
    assert_that((Left(2)+Right(3)).is_right()).is_false()
    assert_that((Left(2)+Right(3)).unwrap()).is_equal_to(2)
    

    assert_that((Right(2)+Left(3)).is_left()).is_true()
    assert_that((Right(2)+Left(3)).is_right()).is_false()
    assert_that((Right(2)+Left(3)).unwrap()).is_equal_to(3)
    
    assert_that((Left(2)+Left(3)).is_left()).is_true()
    assert_that((Left(2)+Left(3)).unwrap()).is_equal_to(2)
    
    assert_that((Left(3)+Left(2)).is_left()).is_true()
    assert_that((Left(3)+Left(2)).unwrap()).is_equal_to(3)

    assert_that((Right(2)+Right(3)).is_right()).is_true()
    assert_that((Right(2)+Right(3)).unwrap()).is_equal_to(5)

@pytest.mark.either
def test_either_map():
    v = Left(2).map(lambda x: x+3)
    assert_that(v.is_left()).is_true()
    assert_that(v.is_right()).is_false()
    assert_that(v.unwrap()).is_equal_to(2)

    v = Right(2).map(lambda x: x+3)
    assert_that(v.is_right()).is_true()
    assert_that(v.is_left()).is_false()
    assert_that(v.unwrap()).is_equal_to(5)
    
    v = Right("test").map(lambda x: len(x)+3)
    assert_that(v.is_right()).is_true()
    assert_that(v.is_left()).is_false()
    assert_that(v.unwrap()).is_equal_to(7)

@pytest.mark.either
def test_either_applicative():
    x = Right.unit(42)
    f = lambda x: x * 1
    m = Right.pure(f).apply(x)
    assert_that(m.unwrap()).is_equal_to(x.map(f).unwrap())
    res = m.match(
         left=lambda: fail('The monad should be Just.'),
         right=lambda x: x
    )
    assert_that(res).is_equal_to(42)

@pytest.mark.either
def test_either_monad():
    v = Left.unit("error").bind(lambda x: x+" df").bind(lambda y: y+"  sc")
    assert_that(v.is_left()).is_true()
    assert_that(v.unwrap()).is_equal_to("error")    
    
    v = Right.unit("error").bind(lambda x: x+" df").bind(lambda y: y+"  sc")
    assert_that(v.is_right()).is_true()
    assert_that(v.unwrap()).is_equal_to("error df  sc")    
    
    v = Right.unit(42).bind(lambda x: x/0).bind(lambda y: y+2)
    assert_that(v.is_left()).is_true()
    assert_that(v.unwrap()).is_instance_of(Exception)    