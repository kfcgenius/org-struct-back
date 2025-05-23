from abc import ABC, abstractmethod
from uuid import UUID, uuid4

from org_struct_back.service.models import NodeModel
from org_struct_back.storage.database import Database
from org_struct_back.storage.entities import NodeEntity
from org_struct_back.storage.node_repository import NodeRepository


class NodeService(ABC):
    @abstractmethod
    def get_by_id(self, node_id: UUID, depth: int) -> NodeModel | None:
        pass

    @abstractmethod
    def get_by_name(self, name: str, depth: int) -> list[NodeModel]:
        pass

    @abstractmethod
    def get_all(self) -> list[NodeModel]:
        pass

    @abstractmethod
    def create(self, node_name: str, parent_id: UUID | None) -> NodeModel:
        pass

    @abstractmethod
    def update(self, node_id: UUID, name: str, parent_id: UUID | None) -> NodeModel | None:
        pass


class NodeServiceImpl(NodeService):
    def __init__(self, repository: NodeRepository, db: Database) -> None:
        self._repository = repository
        self._db = db

    def get_by_id(self, node_id: UUID, depth: int) -> NodeModel | None:
        with self._db() as session:
            node_entity = self._repository.get_by_id(session, node_id, depth)
            if node_entity is None:
                return None
            node_model = NodeModel.model_validate(node_entity)
            return node_model

    def get_by_name(self, name: str, depth: int) -> list[NodeModel]:
        with self._db() as session:
            node_entities = self._repository.get_by_name(session, name, depth)
            node_models = [NodeModel.model_validate(i) for i in node_entities]
            return node_models

    def get_all(self) -> list[NodeModel]:
        with self._db() as session:
            node_entities = self._repository.get_all(session)
            node_models = [NodeModel.model_validate(i) for i in node_entities]
            return node_models

    def create(self, name: str, parent_id: UUID | None) -> NodeModel:
        with self._db() as session:
            if parent_id is not None:
                parent_node_entity = self._repository.get_by_id(session, parent_id, 0)
                if parent_node_entity is None:
                    return None
            node_entity = NodeEntity(id=uuid4(), name=name, parent_id=parent_id)
            self._repository.create(session, node_entity)
            session.commit()
            node_model = NodeModel.model_validate(node_entity)
            return node_model

    def update(self, node_id: UUID, name: str, parent_id: UUID | None) -> NodeModel | None:
        if node_id == parent_id:
            return None
        with self._db() as session:
            node_entity = self._repository.get_by_id(session, node_id, 1)
            if node_entity is None:
                return None
            if parent_id is not None:
                parent_node_entity = self._repository.get_by_id(session, parent_id, 0)
                if parent_node_entity is None:
                    return None
                node_entity.parent_id = parent_id
            node_entity.name = name
            session.commit()
            node_model = NodeModel.model_validate(node_entity)
            return node_model
