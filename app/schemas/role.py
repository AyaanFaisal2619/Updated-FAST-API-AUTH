from pydantic import BaseModel
import uuid

class RoleBase(BaseModel):
    name: str

class RoleCreate(RoleBase):
    pass

class RoleUpdate(RoleBase):
    pass

class RoleOut(RoleBase):
    id: uuid.UUID  # Changed from int to UUID

    class Config:
        from_attributes = True
