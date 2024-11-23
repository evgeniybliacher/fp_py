from dataclasses import dataclass
from typing import Generic, Optional, Self, TypeVar

from fp_py.types import typed_lambda, untyped_lambda

T = TypeVar('T')
R = TypeVar('R')
Func = TypeVar('F', bound = typed_lambda[T])
Action = TypeVar('Action', bound=untyped_lambda)

class Maybe(Generic[T]):
    def __init__(self, value:Optional[T]):
        self._value = value

    def is_none(self) -> bool:
        return self._value is None
    
    def is_some(self) -> bool:
        return self._value is not None
    
    def match(self, none: Action, some: Func)-> Self:
        return some(self._value) if self.is_some() else none()


    def bind(self, func:Func) -> Self:
        return Maybe(func(self._value)) if self.is_some() else Maybe(None)

    def unwrap(self)->Optional[T]:
        return self._value
   
    @classmethod
    def Nothing(cls) -> Self:
        return cls(None)

    @classmethod
    def Some(cls, value: T) -> Self:
        return cls(value)
    
    @classmethod
    def wrap(cls, value:Optional[T])->Self:
        return  Maybe.Some(value) if value is not None else Maybe.Nothing()

def Some[T](value: T)-> Maybe[T]:
    return Maybe[T].wrap(value)

def Nothing() -> Maybe[T]:
    return Maybe.wrap(None)