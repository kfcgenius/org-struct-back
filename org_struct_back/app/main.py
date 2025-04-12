from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from org_struct_back.api.node_router import node_router
from org_struct_back.app.dependency import build_container
from org_struct_back.storage.database import Database

container = build_container()
db: Database = container.resolve(Database)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[Any, Any]:
    yield
    db.shutdown()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.ioc_container = container

app.include_router(node_router)
