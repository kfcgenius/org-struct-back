from collections.abc import Callable

from punq import Container

from org_struct_back.app.server import Server, ServerImpl
from org_struct_back.settings.server_settings import ServerSettings


def build_container() -> Container:
    container = Container()

    _register_settings(container, ServerSettings)

    container.register(Server, factory=ServerImpl)

    return container


def _register_settings(c: Container, cls: Callable) -> None:
    c.register(cls, factory=lambda: cls())
