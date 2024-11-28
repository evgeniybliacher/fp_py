import pytest
from fp_py.utils.lambda_calculus import *

from  assertpy import assert_that

@pytest.mark.lambdacalculus
def test_identity():
    assert_that(identity(4)).is_equal_to(4)
    assert_that(identity(lambda x: x+ 2)(4)).is_equal_to(6)

@pytest.mark.lambdacalculus
def test_select_first():
    assert_that(select_first(1)(2)).is_equal_to(1)
    assert_that(select_first(lambda x: x+2)(2)(3)).is_equal_to(5)
    assert_that(select_first(2)(lambda x: x+2)).is_equal_to(2)
    assert_that(select_first(lambda x: x*3)(lambda x: x+2)(3)).is_equal_to(9)

@pytest.mark.lambdacalculus
def test_iff_true():
    assert_that(iff(true, 1, 2)).is_equal_to(1)

@pytest.mark.lambdacalculus
def test_iff_false():
    assert_that(iff(false, 1, 2)).is_equal_to(2)

@pytest.mark.lambdacalculus
def test_printl_zero():
    assert_that(printl(zero)).is_equal_to(0)
        
@pytest.mark.lambdacalculus
def test_printl_one():
    assert_that(printl(one)).is_equal_to(1)

@pytest.mark.lambdacalculus
def test_succ_zero():
    assert_that(printl(succ(zero))).is_equal_to(1)