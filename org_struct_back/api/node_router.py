from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Query, status, HTTPException

from org_struct_back.api.dtos import NodeCreateDto, NodeDto, InputError, NodeUpdateDto
from org_struct_back.app.ioc_service import Inject
from org_struct_back.service.domain import NodeService

node_router = APIRouter(prefix="/api/v1/nodes", tags=["Nodes"])


@node_router.get("")
def get(service: Annotated[NodeService, Inject(NodeService)],
        name: Annotated[str, Query()] = "",
        depth: Annotated[int, Query(ge=0, le=100)] = 0) -> list[NodeDto]:
    node_models = service.get_all() if len(name) == 0 else service.get_by_name(name, depth)
    node_dtos = [NodeDto.model_validate(i) for i in node_models]
    return node_dtos


@node_router.post("")
def post(node_create: NodeCreateDto, service: Annotated[NodeService, Inject(NodeService)]) -> NodeDto:
    node_model = service.create(node_create.name, node_create.parent_id)
    if node_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=[InputError(msg="Failed to create node").model_dump()])
    node_dto = NodeDto.model_validate(node_model)
    return node_dto


@node_router.put("/{node_id}")
def put_by_id(node_id: UUID, node_create: NodeUpdateDto,
              service: Annotated[NodeService, Inject(NodeService)]) -> NodeDto:
    node_model = service.update(node_id, node_create.name, node_create.parent_id)
    if node_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=[InputError(msg="Failed to create node").model_dump()])
    node_dto = NodeDto.model_validate(node_model)
    return node_dto


@node_router.get("/{node_id}")
def get_by_id(node_id: UUID, service: Annotated[NodeService, Inject(NodeService)],
              depth: Annotated[int, Query(ge=0, le=100)] = 0) -> NodeDto:
    node_model = service.get_by_id(node_id, depth)
    if node_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=[InputError(msg="Node not found").model_dump()])
    node_dto = NodeDto.model_validate(node_model)
    return node_dto
