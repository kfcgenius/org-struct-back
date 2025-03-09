from fastapi import FastAPI

from org_struct_back.api.node_router import node_router
from org_struct_back.app.dependency import build_container
from org_struct_back.settings.server_settings import ServerSettings

container = build_container()
settings: ServerSettings = container.resolve(ServerSettings)

app = FastAPI(title=settings.name)

app.state.ioc_container = container

app.include_router(node_router)
