from typing import Callable


class typed_lambda[*Ts]:
    def __new__[U](cls, f: Callable[[*Ts], U], /) -> Callable[[*Ts], U]:
        return f
    

class untyped_lambda:
    def __new__[U](cls, f:Callable[[], U], /) -> Callable[[], U]:
        return f
