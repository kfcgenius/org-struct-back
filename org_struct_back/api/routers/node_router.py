from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Query, Response, status

from org_struct_back.api.dtos.dtos import Error, Meta, ResponseWrapper
from org_struct_back.api.dtos.node_dtos import NodeDto
from org_struct_back.app.ioc_service import Service
from org_struct_back.service.domain.node_service import NodeService

node_router_v1 = APIRouter(prefix="/v1/nodes")


@node_router_v1.get("")
def get_by_name(
    name: Annotated[str, Query(min_length=1)],
    depth: Annotated[int, Query(min_length=1, max_length=100)],
    service: Annotated[NodeService, Service(NodeService)],
    response: Response,
) -> ResponseWrapper[NodeDto]:
    node = service.find_by_name(name, depth)
    if node is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return ResponseWrapper(
            meta=Meta(success=False), errors=[Error(code="000", messsage="Sorry")]
        )

    node_json = node.model_dump()
    node_dto = NodeDto.model_validate(node_json)

    response.status_code = status.HTTP_200_OK
    return ResponseWrapper(meta=Meta(success=True), data=node_dto)


@node_router_v1.get("/{node_id}")
def get_by_id(
    node_id: UUID,
    depth: Annotated[int, Query(min_length=1, max_length=100)],
    service: Annotated[NodeService, Service(NodeService)],
    response: Response,
) -> ResponseWrapper[NodeDto]:
    node = service.get_by_id(node_id, depth)
    if node is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return ResponseWrapper(
            meta=Meta(success=False), errors=[Error(code="000", messsage="Sorry")]
        )

    node_json = node.model_dump()
    node_dto = NodeDto.model_validate(node_json)

    response.status_code = status.HTTP_200_OK
    return ResponseWrapper(meta=Meta(success=True), data=node_dto)
