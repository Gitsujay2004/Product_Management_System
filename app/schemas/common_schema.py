from typing import Generic, TypeVar

from pydantic import BaseModel


T = TypeVar("T")


class MessageResponse(BaseModel):
    message: str


class DataResponse(BaseModel, Generic[T]):
    message: str
    data: T