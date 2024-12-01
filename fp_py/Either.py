
from abc import abstractmethod
from functools import reduce, partial

from typing import Callable, Any, Optional, TypeVar, cast

from fp_py.types.lambda_types import typed_lambda, untyped_lambda


from .types import Applicative
from .types import Functor
from .types import Monoid
from .types import Monad

TSource = TypeVar("TSource")
TResult = TypeVar("TResult")
TError = TypeVar("TError")

class Either[TError, TSource]:
    """The Either Monad.

    Represents either a successful computation, or a computation that
    has failed.
    """


    @abstractmethod
    def __add__(self, other: "Either[TError,TSource]") -> "Either[TError,TSource]":
        ...

    @abstractmethod
    def map(self, _: typed_lambda[TSource, TResult]) -> "Either[TError,TResult]":
        ...

    @classmethod
    def pure(cls, value: typed_lambda[TSource, TResult]) -> "Either[TError, typed_lambda[TSource, TResult]]":
        ...

    @abstractmethod
    def apply(self: "Either[TError, typed_lambda[TSource, TResult]]", something: "Either[TError, TSource]") -> "Either[TError,TResult]":
        ...

    @classmethod
    @abstractmethod
    def unit(cls, value: TSource) -> "Either[TError, TSource]":
        ...

    @abstractmethod
    def bind(self, fn: typed_lambda[TSource, "Either[TError, TSource]"]) -> "Either[TError, TResult]":
        ...
    @abstractmethod
    def bind(self, func: typed_lambda[TSource, TResult]) -> "Either[TError,TResult]":
        ...

    # Utilities Section
    # =================
    @abstractmethod
    def is_left(self) -> bool:
        return False

    @abstractmethod
    def is_right(self) -> bool:
        return True



    @classmethod
    def concat(cls, xs):
        """mconcat :: [m] -> m

        Fold a list using the monoid. For most types, the default
        definition for mconcat will be used, but the function is
        included in the class definition so that an optimized version
        can be provided for specific types.
        """

        def reducer(a, b):
            return a + b

        return reduce(reducer, xs, cls.empty())

    def __rmod__(self, fn):
        """Infix version of map.

        Haskell: <$>

        Example:
        >>> (lambda x: x+2) % Just(40)
        42

        Returns a new Functor.
        """
        return self.map(fn)
    
    def match(self, left: typed_lambda[TError], right: typed_lambda[TResult]):
        return left(self._value) if self.is_left() else right(self._value)
    
    def unwrap(self)->TSource|TResult|TError:
        return self._value

    def contoled_map(self, mapper: typed_lambda[TSource, TResult])-> "Either[TError, TResult]":
        try:
            result = mapper(self._value)
            return Left(result) if result is None else Right(result)
        except Exception as ex:
            return Left(ex)
        
class Left(Either[TError, TSource]):
    def __init__(self, value : TError) -> None:
        self._value = value

    def is_left(self) -> bool:
        return True

    def is_right(self) -> bool:
        return False
    
    def __add__(self, other: "Either[TError,TSource]") -> "Either[TError,TSource]":
        return Left(self._value) 

    def map(self, mapper : typed_lambda[TSource, TResult]) -> "Either[TError,TResult]":
        return Left(self._value)

    @classmethod
    def pure(cls, value: typed_lambda[TSource, TResult]) -> "Either[TError, typed_lambda[TSource, TResult]]":
        return Right(value)

    def apply(self: "Either[typed_lambda[TSource, TResult]]", something: Either[TError, TSource]) -> Either[TError, TResult]:
        return Left(self._value)

    def bind(self, fn: typed_lambda[TSource, "Either[TError, TSource]"]) -> "Either[TError, TResult]":
        return Left(self._value)
    
    def bind(self, func: typed_lambda[TSource, TResult]) -> "Either[TError,TResult]":
        return Left(self._value)

    @classmethod
    def unit(cls, value: TSource) -> "Either[TError, TSource]":
        return Left(value)
    
class Right(Either[TError, TSource]):
    def __init__(self, value: TSource) -> None:
        self._value = value
    

    def is_left(self) -> bool:
        return False

    def is_right(self) -> bool:
        return True
 
    def __add__(self, other: "Either[TError,TSource]") -> "Either[TError,TSource]":
        if other.is_left():
            return Left(other._value)
        return other.map(
            lambda other_value: cast(Any, self._value) + other_value if hasattr(self._value, "__add__") else Left()
        )

    def map(self, mapper : typed_lambda[TSource, TResult]) -> "Either[TError,TResult]":
        return self.contoled_map(mapper)

    @classmethod
    def pure(cls, value: typed_lambda[TSource, TResult]) -> "Either[TError, typed_lambda[TSource, TResult]]":
        return Right(value)
    
    def apply(self: "Either[TError, typed_lambda[TSource, TResult]]", something: Either[TError,TSource]) -> Either[TError, TResult]:
        def mapper(other_value):
            try:
                return self._value(other_value)
            except TypeError:
                return partial(self._value, other_value)
        return something.map(mapper)
    
    @classmethod
    def unit(cls, value: TSource) -> "Either[TError, TSource]":
        return Right(value)
    
    def bind(self, func: typed_lambda[TSource, "Either[TError, TSource]"]) -> "Either[TError, TResult]":
        return self.contoled_map(func)
    
    def bind(self, func: typed_lambda[TSource, TResult]) -> "Either[TError,TResult]":
        return self.contoled_map(func)
    
    @classmethod
    def unit(cls, value: TSource) -> "Either[TError, TSource]":
        return Right(value)
    
assert(isinstance(Either, Functor))
assert(isinstance(Either, Applicative))
assert(isinstance(Either, Monad))

assert(isinstance(Right, Functor))
assert(isinstance(Right, Applicative))
assert(isinstance(Right, Monad))

assert(isinstance(Left, Functor))
assert(isinstance(Left, Applicative))
assert(isinstance(Left, Monad))