from uuid import UUID
from datetime import datetime

from pydantic import BaseModel


class SessionCreate(BaseModel):
    user_id: UUID
    token: str
    expires_at: datetime


class SessionUpdate(BaseModel):
    token: str
    expires_at: datetime