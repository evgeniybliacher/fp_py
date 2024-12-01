import pytest

from fp_py.Maybe import Just, Maybe, Nothing
from assertpy import assert_that,fail


pure = Just.pure
unit = Just.unit

@pytest.mark.maybe
def test_maybe_nothing():
    v = Nothing()
    assert_that(v.is_nothing()).is_true()
    assert_that(v.is_just()).is_false()

@pytest.mark.maybe
def test_maybe_just():
    v = Just(42)
    i = Just.pure(lambda x: x+3)
    assert_that(v.is_just()).is_true()
    assert_that(i.is_just()).is_true()
    assert_that(v.is_nothing()).is_false()
    assert_that(i.is_nothing()).is_false()

@pytest.mark.maybe
def test_maybe_applicative():
    x = unit(42)
    f = lambda x: x * 1
    m = pure(f).apply(x)
    assert_that(m).is_equal_to(x.map(f))
    res = m.match(
         nothing=lambda: fail('The monad should be Just.'),
         just=lambda x: x
    )
    assert_that(res).is_equal_to(42)

@pytest.mark.maybe
def test_maybe_monad():
    assert_that(unit(42).bind(lambda x: x+ 2).bind(lambda x: x*2).unwrap()).is_equal_to(88)
    assert_that(unit(42).bind(lambda x: x+ 2).bind(lambda x: None).is_nothing()).is_true()
    assert_that(unit(None).bind(lambda x: x+ 2).bind(lambda x: 42).is_nothing()).is_true()

@pytest.mark.maybe
def test_maybe_semigroup():
    v = unit(42)
    i = unit(28)
    z = unit(None)
    k = v+i
    j = i+z
    assert_that(k.is_just()).is_true()
    assert_that(k.unwrap()).is_equal_to(70)
    assert_that(j.is_just()).is_true()
    assert_that(j.is_nothing()).is_false()
    assert_that(j.unwrap()).is_equal_to(28)
    assert_that((Nothing()+Nothing()).is_nothing()).is_true()

@pytest.mark.maybe
def test_maybe_monoid():
    v = unit(42)
    i = v + Nothing().empty() + Just.empty()
    assert_that(i.is_just()).is_true()
    assert_that(i.is_nothing()).is_false()
    assert_that(i.unwrap()).is_equal_to(42)