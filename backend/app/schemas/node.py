from datetime import datetime

from pydantic import BaseModel, HttpUrl


class NodeCreate(BaseModel):
    name: str
    base_url: str
    region: str | None = None
    description: str | None = None
    api_token: str | None = None


class NodeOut(BaseModel):
    id: int
    name: str
    base_url: str
    region: str | None
    description: str | None
    created_at: datetime

    class Config:
        from_attributes = True
