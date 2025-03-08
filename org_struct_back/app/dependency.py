from collections.abc import Callable
from typing import Any

from punq import Container

from org_struct_back.service.domain.node_service import NodeService, NodeServiceImpl
from org_struct_back.settings.node_settings import NodeSettings
from org_struct_back.settings.server_settings import ServerSettings


def build_container() -> Container:
    container = Container()

    _register_settings(container, ServerSettings)
    _register_settings(container, NodeSettings)

    container.register(NodeService, factory=NodeServiceImpl)

    return container


def _register_settings(c: Container, cls: Callable[..., Any]) -> None:
    c.register(cls, factory=lambda: cls())
