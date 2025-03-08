from uuid import UUID

from pydantic import BaseModel


class NodeSearchDto(BaseModel):
    id: UUID | None = None
    name: str | None = None
    depth: int = 1


class NodeDto(BaseModel):
    id: UUID
    name: str
    parent_id: UUID
    children: list["NodeDto"]
