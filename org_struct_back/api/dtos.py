from uuid import UUID

from pydantic import BaseModel, ConfigDict


class InputError(BaseModel):
    type: str = "input_error"
    msg: str


class NodeDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    name: str
    parent_id: UUID | None
    children: dict[str, "NodeDto"]


class NodeCreateDto(BaseModel):
    name: str
    parent_id: UUID | None
