from pydantic import BaseModel
from uuid import UUID

class PermissionBase(BaseModel):
    name: str
    description: str

class PermissionCreate(PermissionBase):
    pass

class PermissionUpdate(PermissionBase):
    name: str | None = None
    description: str | None = None

class PermissionOut(PermissionBase):
    id: UUID  # Changed to UUID

    class Config:
        from_attributes = True
