from fastapi import APIRouter

from org_struct_back.api.routers.node_router import node_router_v1

router = APIRouter(prefix="/api")

router.include_router(node_router_v1)
