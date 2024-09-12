from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid

from app.crud import permissions
from app.schemas.permission import PermissionCreate, PermissionUpdate, PermissionOut
from app.api.deps import get_db

router = APIRouter()

@router.post("/permissions", response_model=dict)
async def create_permission_endpoint(permission: PermissionCreate, db: Session = Depends(get_db)):
    existing_permission = permissions.get_permission_by_name(db, permission.name)
    if existing_permission:
        raise HTTPException(status_code=400, detail="Permission already exists")
    
    new_permission = permissions.create_permission(db, permission)
    return {"message": f"Permission '{new_permission.name}' created successfully"}

@router.get("/", response_model=List[PermissionOut])
def read_permissions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    permissions_list = permissions.get_permissions(db, skip=skip, limit=limit)
    return permissions_list

@router.get("/{permission_id}", response_model=PermissionOut)
def read_permission(permission_id: uuid.UUID, db: Session = Depends(get_db)):
    db_permission = permissions.get_permission(db, permission_id)
    if db_permission is None:
        raise HTTPException(status_code=404, detail="Permission not found")
    return db_permission

@router.put("/{permission_id}", response_model=PermissionOut)
def update_permission(permission_id: uuid.UUID, permission: PermissionUpdate, db: Session = Depends(get_db)):
    updated_permission = permissions.update_permission(db, permission_id, permission)
    if updated_permission is None:
        raise HTTPException(status_code=404, detail="Permission not found")
    return updated_permission

@router.delete("/{permission_id}", response_model=PermissionOut)
def delete_permission(permission_id: uuid.UUID, db: Session = Depends(get_db)):
    deleted_permission = permissions.delete_permission(db, permission_id)
    if deleted_permission is None:
        raise HTTPException(status_code=404, detail="Permission not found")
    return deleted_permission
