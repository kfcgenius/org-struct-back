from typing import Annotated

from fastapi import APIRouter, Response, status

from org_struct_back.api.dtos.dtos import Error, Meta, ResponseWrapper
from org_struct_back.api.dtos.node_dtos import NodeDto, NodeSearchDto
from org_struct_back.app.ioc_service import Service
from org_struct_back.service.domain.node_service import NodeService
from org_struct_back.settings.node_settings import NodeSettings

node_router_v1 = APIRouter(prefix="/v1/nodes")


@node_router_v1.post("/search")
def search_node(
    node_search: NodeSearchDto,
    settings: Annotated[NodeSettings, Service(NodeSettings)],
    service: Annotated[NodeService, Service(NodeService)],
    response: Response,
) -> ResponseWrapper[NodeDto]:
    if node_search.depth < settings.min_depth or node_search.depth > settings.max_depth:
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return ResponseWrapper(meta=Meta(success=False), errors=[Error(code="000", messsage="Sorry")])

    if not node_search.id and not node_search.name:
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return ResponseWrapper(meta=Meta(success=False), errors=[Error(code="000", messsage="Sorry")])

    if node_search.id:
        node = service.get_by_id(node_search.id, node_search.depth)
    elif node_search.name:
        node = service.find_by_name(node_search.name, node_search.depth)

    if node is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return ResponseWrapper(meta=Meta(success=False), errors=[Error(code="000", messsage="Sorry")])

    node_json = node.model_dump()
    node_dto = NodeDto.model_validate(node_json)

    response.status_code = status.HTTP_200_OK
    return ResponseWrapper(meta=Meta(success=True), data=node_dto)
