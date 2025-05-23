from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Query, status, HTTPException

from org_struct_back.api.dtos import NodeCreateDto, NodeDto, InputError, NodeUpdateDto
from org_struct_back.app.ioc_service import Inject
from org_struct_back.service.domain import NodeService

node_router = APIRouter(prefix="/api/v1/nodes", tags=["Nodes"])


@node_router.get("")
def get_by_name(name: Annotated[str, Query(min_length=1)], service: Annotated[NodeService, Inject(NodeService)],
                depth: Annotated[int, Query(ge=0, le=100)] = 0) -> NodeDto:
    node_model = service.find_by_name(name, depth)
    if node_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=[InputError(msg="Node not found").model_dump()])
    node_dto = NodeDto.model_validate(node_model)
    return node_dto


@node_router.post("")
def post(node_create: NodeCreateDto, service: Annotated[NodeService, Inject(NodeService)]) -> NodeDto:
    node_model = service.create(node_create.name, node_create.parent_id)
    if node_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=[InputError(msg="Failed to create node").model_dump()])
    node_dto = NodeDto.model_validate(node_model)
    return node_dto


@node_router.put("/{node_id}")
def post(node_id: UUID, node_create: NodeUpdateDto, service: Annotated[NodeService, Inject(NodeService)]) -> NodeDto:
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
