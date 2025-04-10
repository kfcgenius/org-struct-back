import functools
from collections.abc import Callable
from typing import Any

from fastapi import Depends, Request


def Inject[T](t: T) -> Any:
    def resolver(t: T, request: Request) -> Callable[..., T]:
        return request.app.state.ioc_container.resolve(t)
    return Depends(functools.partial(resolver, t))
