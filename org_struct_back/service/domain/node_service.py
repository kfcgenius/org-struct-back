from abc import ABC, abstractmethod
from uuid import UUID, uuid4

from org_struct_back.service.models.node_models import NodeModel


class NodeService(ABC):
    @abstractmethod
    def get_by_id(self, node_id: UUID, depth: int) -> NodeModel | None:
        pass

    @abstractmethod
    def find_by_name(self, node_name: str, depth: int) -> NodeModel | None:
        pass


class NodeServiceImpl(NodeService):
    def get_by_id(self, node_id: UUID, _: int) -> NodeModel | None:
        return NodeModel(
            id=node_id,
            parent_id=uuid4(),
            name="",
            children=[
                NodeModel(
                    id=uuid4(),
                    parent_id=uuid4(),
                    name="",
                    children=[NodeModel(id=uuid4(), parent_id=uuid4(), name="", children=[])],
                )
            ],
        )

    def find_by_name(self, node_name: str, _: int) -> NodeModel | None:
        return NodeModel(id=uuid4(), parent_id=uuid4(), name=node_name, children=[])
