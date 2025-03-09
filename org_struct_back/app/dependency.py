from collections.abc import Callable
from typing import Any

from punq import Container

from org_struct_back.service.domain import NodeService, NodeServiceImpl
from org_struct_back.settings.database_settings import DatabaseSettings
from org_struct_back.settings.server_settings import ServerSettings
from org_struct_back.storage.database import Database, DatabaseImpl
from org_struct_back.storage.node_repository import NodeRepository, NodeRepositoryImpl


def build_container() -> Container:
    container = Container()

    _register_settings(container, DatabaseSettings)
    _register_settings(container, ServerSettings)

    container.register(Database, factory=DatabaseImpl)
    container.register(NodeRepository, factory=NodeRepositoryImpl)
    container.register(NodeService, factory=NodeServiceImpl)

    return container


def _register_settings(c: Container, cls: Callable[..., Any]) -> None:
    c.register(cls, factory=lambda: cls())
