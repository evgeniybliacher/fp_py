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


class Maybe[TSource]:
    """Encapsulates an optional value.

    The Maybe type encapsulates an optional value. A value of type
    Maybe a either contains a value of (represented as Just a), or it is
    empty (represented as Nothing). Using Maybe is a good way to deal
    with errors or exceptional cases without resorting to drastic
    measures such as error.
    """

    @classmethod
    def empty(cls) -> "Maybe[TSource]":
        return Nothing()

    @abstractmethod
    def __add__(self, other: "Maybe[TSource]") -> "Maybe[TSource]":
        ...

    @abstractmethod
    def map(self, mapper: typed_lambda[TSource, TResult]) -> "Maybe[TResult]":
        ...

    @classmethod
    def pure(cls, value: typed_lambda[TSource, TResult]) -> "Maybe[Callable[[TSource], TResult]]":
        ...

    @abstractmethod
    def apply(self: "Maybe[typed_lambda[TSource, TResult]]", something: "Maybe[TSource]") -> "Maybe[TResult]":
        ...

    @classmethod
    @abstractmethod
    def unit(cls, a: TSource) -> "Maybe[TSource]":
        ...

    @abstractmethod
    def bind(self, fn: typed_lambda[TSource, "Maybe[TResult]"]) -> "Maybe[TResult]":
        ...

    # Utilities Section
    # =================
    @abstractmethod
    def is_just(self) -> bool:
        return False

    @abstractmethod
    def is_nothing(self) -> bool:
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
    
    def match(self, nothing: untyped_lambda, just: typed_lambda[TSource]):
        if self.is_nothing():
            return nothing()
        return just(self._value)
    
    def selector(self, value: TSource) -> "Maybe[TSource]":
        return Just(value) if value is not None else Nothing()
    
    def unwrap(self)->Optional[TSource]:
        return self._value

class Nothing(Maybe[TSource]):

    """Represents an empty Maybe.

    Represents an empty Maybe that holds nothing (in which case it has
    the value of Nothing).
    """

    # Monoid Section
    # ==============

    def __add__(self, other: Maybe[TSource]) -> Maybe[TSource]:
        # m `append` Nothing = m
        return other

    # Functor Section
    # ===============

    def map(self, mapper: typed_lambda[TSource,TResult]) -> Maybe[TResult]:
        return Nothing()

    # Applicative Section
    # ===================

    @classmethod
    def pure(cls, value: typed_lambda[TSource, TResult]) -> Maybe[typed_lambda[TSource, TResult]]:
        return Nothing()

    def apply(self: "Nothing[typed_lambda[TSource, TResult]]", something: Maybe[TSource]) -> Maybe[TResult]:
        return Nothing()

    # Monad Section
    # =============

    @classmethod
    def unit(cls, value: TSource) -> Maybe[TSource]:
        return cls()

    def bind(self, func: typed_lambda[TSource, Maybe[TResult]]) -> Maybe[TResult]:
        """Nothing >>= f = Nothing

        Nothing in, Nothing out.
        """

        return Nothing()

    # Utilities Section
    # =================

    def is_just(self) -> bool:
        return False

    def is_nothing(self) -> bool:
        return True

    # Operator Overloads Section
    # ==========================

    def __eq__(self, other) -> bool:
        return isinstance(other, Nothing)

    def __str__(self) -> str:
        return "Nothing"

    def __repr__(self) -> str:
        return str(self)


class Just(Maybe[TSource]):

    """A Maybe that contains a value.

    Represents a Maybe that contains a value (represented as Just a).
    """ 
    def __init__(self, value: TSource)->Maybe[TSource]:
        self._value = value

    # Monoid Section
    # ==============

    def __add__(self, other: Maybe[TSource]) -> Maybe[TSource]:
        if isinstance(other, Nothing):
            return self
        return other.map(
            lambda other_value: cast(Any, self._value) + other_value if hasattr(self._value, "__add__") else Nothing()
        )
        

    # Functor Section
    # ===============

    def map(self, mapper: typed_lambda[TSource,TResult]) -> Maybe[TResult]:
        # fmap f (Just x) = Just (f x)
        result = mapper(self._value)
        return self.selector(result)

    # Applicative Section
    # ===================

    @classmethod
    def pure(cls, value: typed_lambda[TSource, TResult]) -> Maybe[typed_lambda[TSource, TResult]]:
        return  Just(value) if value is not None else Nothing()

    def apply(self: "Just[typed_lambda[TSource, TResult]]", something: Maybe[TSource]) -> Maybe[TResult]:
        def mapper(other_value):
            try:
                return self._value(other_value)
            except TypeError:
                return partial(self._value, other_value)
        return something.map(mapper)

    # Monad Section
    # =============

    @classmethod
    def unit(cls, value: TSource) -> Maybe[TSource]:
        return  Just(value) if value is not None else Nothing()

    def bind(self, func: typed_lambda[TSource, Maybe[TResult]]) -> Maybe[TResult]:
        """Just x >>= f = f x."""

        return func(self._value)
    
    def bind(self, func: typed_lambda[TSource, TResult]) -> Maybe[TResult]:
        """Just x >>= f = f x."""

        return Just.unit(func(self._value))
    
    # Utilities Section
    # =================

    def is_just(self) -> bool:
        return True

    def is_nothing(self) -> bool:
        return False

    # Operator Overloads Section
    # ==========================
    def __bool__(self) -> bool:
        return bool(self._value)
    
    def __eq__(self, other) -> bool:
        if isinstance(other, Nothing):
            return False
        return bool(other.map(lambda other_value: other_value == self._value))

    def __str__(self) -> str:
        return f"Just {self._value}"

    def __repr__(self) -> str:
        return str(self)

assert issubclass(Just, Maybe)
assert issubclass(Nothing, Maybe)

assert isinstance(Maybe, Monoid)
assert isinstance(Maybe, Functor)
assert isinstance(Maybe, Applicative)
assert isinstance(Maybe, Monad)

assert isinstance(Just, Monoid)
assert isinstance(Just, Functor)
assert isinstance(Just, Applicative)
assert isinstance(Just, Monad)

assert isinstance(Nothing, Monoid)
assert isinstance(Nothing, Functor)
assert isinstance(Nothing, Applicative)
assert isinstance(Nothing, Monad)