
from abc import abstractmethod

from typing import Self, TypeVar, Protocol
from typing_extensions import runtime_checkable


TSource = TypeVar('TSource', covariant=True)

@runtime_checkable
class Semigroup(Protocol[TSource]):
    """The Semigroup class is used for types that can be mapped over.

    The set is semigroup if we can  define binary operation:
      a:T -> a->b -> b:T
    """

    @abstractmethod
    def __add__(self, other: TSource) -> Self:
        """Map a function over wrapped values.

        Map knows how to apply functions to values that are wrapped in
        a context.
        """
        ...