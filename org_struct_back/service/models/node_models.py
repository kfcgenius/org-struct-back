from uuid import UUID

from pydantic import BaseModel


class NodeModel(BaseModel):
    id: UUID
    name: str
    parent_id: UUID
    children: list["NodeModel"]
