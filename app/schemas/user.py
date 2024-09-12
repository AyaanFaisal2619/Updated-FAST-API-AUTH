from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class UserBase(BaseModel):
    username: str
    email: Optional[str] = None
    is_active: Optional[bool] = True

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserOut(UserBase):
    id: UUID  # Adjusted to UUID

    class Config:
        orm_mode = True
