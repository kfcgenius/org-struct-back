from pydantic import BaseModel


class Meta(BaseModel):
    success: bool


class Error(BaseModel):
    messsage: str
    code: str


class ResponseWrapper[T: BaseModel](BaseModel):
    data: T | list[T] | None = None
    meta: Meta
    errors: list[Error] = []
