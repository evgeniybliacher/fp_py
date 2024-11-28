from typing import List, Self
import pytest
from  assertpy import assert_that

from fp_py.types.semigroup import Semigroup





class Intg:
    def __init__(self, value:int):
        self.value = value

    def __add__(self, other)-> Self:
        return Intg(self.value + other.getval()) 
    
    def getval(self)->int:
        return self.value

class SemigroupList[T]:
    def __init__(self, init:List[T]):
        self._list = init

    def __add__(self, other)-> Self:
        return SemigroupList(self._list + other.getval())

    def getval(self) -> List[T]:
        return self._list


def test_int_semigroup():
    assert_that(Intg).is_instance_of(Semigroup)
    assert_that((Intg(4)+Intg(5)).getval()).is_equal_to(9)

def test_list_semigroup():
    assert_that(SemigroupList).is_instance_of(Semigroup)
    assert_that((SemigroupList([4,5,6])+SemigroupList([1,2,3])).getval()).is_length(6)