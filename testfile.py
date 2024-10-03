from typing import Callable, ParamSpec, Concatenate, TypeVar

Param = ParamSpec("Param")
RetType = TypeVar("RetType")

def get_authenticated_user()->str:
    return "John"

def inject_user() -> Callable[[Callable[Param, RetType]], Callable[Concatenate[str, Param], RetType]]:
    def decorator(func: Callable[Param, RetType]) -> Callable[Concatenate[str, Param], RetType]:
        def wrapper(user: str, *args:Param.args, **kwargs:Param.kwargs) -> RetType:
            user = get_authenticated_user()
            if user is None:
                raise Exception("Don't!")
            return func(*args, **kwargs)

        return wrapper

    return decorator


@inject_user()
def foo(a: int) -> bool:
    return bool(a % 2)


reveal_type(foo)  #  # I: Revealed type is "def (builtins.str, a: builtins.int) -> builtins.bool"

foo("user", 2)  # Type check OK
foo("no!")  # E: Missing positional argument "a" in call to "foo"  [call-arg]
foo(3)  # # E: Missing positional argument "a" in call to "foo"  [call-arg] # E: Argument 1 to "foo" has incompatible type "int"; expected "str"  [arg-type]
