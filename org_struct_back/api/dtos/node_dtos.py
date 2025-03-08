from uuid import UUID

from pydantic import BaseModel


class NodeDto(BaseModel):
    id: UUID
    name: str
    parent_id: UUID
    children: list["NodeDto"]
