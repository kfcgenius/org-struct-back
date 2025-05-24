from abc import ABC, abstractmethod
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.orm import Session, selectinload

from org_struct_back.storage.entities import NodeEntity


class NodeRepository(ABC):
    @abstractmethod
    def get_by_id(self, session: Session, node_id: UUID, depth: int) -> NodeEntity | None:
        pass

    @abstractmethod
    def get_by_name(self, session: Session, name: str, depth: int) -> list[NodeEntity]:
        pass

    @abstractmethod
    def get_all(self, session: Session) -> list[NodeEntity]:
        pass

    @abstractmethod
    def create(self, session: Session, node: NodeEntity) -> None:
        pass


class NodeRepositoryImpl(NodeRepository):
    def get_by_id(self, session: Session, node_id: UUID, depth: int) -> NodeEntity | None:
        query = select(NodeEntity).filter(NodeEntity.id == node_id)

        if depth > 0:
            current_load = selectinload(NodeEntity.children)
            for _ in range(depth - 1):
                current_load = current_load.selectinload(NodeEntity.children)
            query = query.options(current_load)

        return session.scalars(query).first()

    def get_by_name(self, session: Session, name: str, depth: int) -> list[NodeEntity]:
        query = select(NodeEntity).filter(func.lower(NodeEntity.name).contains(name.lower()))

        if depth > 0:
            current_load = selectinload(NodeEntity.children)
            for _ in range(depth - 1):
                current_load = current_load.selectinload(NodeEntity.children)
            query = query.options(current_load)

        return session.scalars(query).all()

    def get_all(self, session: Session) -> list[NodeEntity]:
        query = select(NodeEntity)
        return session.scalars(query).all()

    def create(self, session: Session, node: NodeEntity) -> None:
        session.add(node)
