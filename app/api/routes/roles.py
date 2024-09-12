from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid

from app.crud import roles
from app.schemas.role import RoleCreate, RoleUpdate, RoleOut
from app.api.deps import get_db

router = APIRouter()

@router.post("/roles", response_model=dict)
async def create_role_endpoint(role: RoleCreate, db: Session = Depends(get_db)):
    existing_role = roles.get_role_by_name(db, role.name)
    if existing_role:
        raise HTTPException(status_code=400, detail="Role already exists")
    
    new_role = roles.create_role(db, role)
    return {"message": f"Role '{new_role.name}' created successfully"}

@router.get("/", response_model=List[RoleOut])
def read_roles(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    roles_list = roles.get_roles(db, skip=skip, limit=limit)
    return roles_list

@router.get("/{role_id}", response_model=RoleOut)
def read_role(role_id: uuid.UUID, db: Session = Depends(get_db)):
    db_role = roles.get_role(db, role_id)
    if db_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return db_role

@router.put("/{role_id}", response_model=RoleOut)
def update_role(role_id: uuid.UUID, role: RoleUpdate, db: Session = Depends(get_db)):
    updated_role = roles.update_role(db, role_id, role)
    if updated_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return updated_role

@router.delete("/{role_id}", response_model=RoleOut)
def delete_role(role_id: uuid.UUID, db: Session = Depends(get_db)):
    deleted_role = roles.delete_role(db, role_id)
    if deleted_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return deleted_role
