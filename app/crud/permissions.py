from uuid import uuid4
from sqlalchemy.orm import Session
from app.db.models import Permission
from app.schemas.permission import PermissionCreate, PermissionUpdate
from fastapi import HTTPException

def get_permission(db: Session, permission_id: str):  # Updated type to UUID string
    return db.query(Permission).filter(Permission.id == permission_id).first()

def get_permission_by_name(db: Session, name: str):
    return db.query(Permission).filter(Permission.name == name).first()

def get_permissions(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Permission).offset(skip).limit(limit).all()

def create_permission(db: Session, permission: PermissionCreate):
    db_permission = get_permission_by_name(db, permission.name)
    if db_permission:
        raise HTTPException(status_code=400, detail="Permission already exists")

    db_permission = Permission(
        id=str(uuid4()),  # Generate UUID
        name=permission.name,
        description=permission.description
    )
    db.add(db_permission)
    db.commit()
    db.refresh(db_permission)
    return db_permission

def update_permission(db: Session, permission_id: str, permission: PermissionUpdate):
    db_permission = get_permission(db, permission_id)
    if not db_permission:
        raise HTTPException(status_code=404, detail="Permission not found")

    if permission.name:
        db_permission.name = permission.name
    if permission.description:
        db_permission.description = permission.description

    db.commit()
    db.refresh(db_permission)
    return db_permission

def delete_permission(db: Session, permission_id: str):
    db_permission = get_permission(db, permission_id)
    if not db_permission:
        raise HTTPException(status_code=404, detail="Permission not found")

    db.delete(db_permission)
    db.commit()
    return db_permission
