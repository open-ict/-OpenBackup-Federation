from datetime import datetime

from pydantic import BaseModel


class BackupOut(BaseModel):
    id: int
    filename: str
    object_name: str
    content_type: str | None
    size: int
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True
