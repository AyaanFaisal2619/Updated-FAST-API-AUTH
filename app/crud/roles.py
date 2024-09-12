from uuid import UUID
from sqlalchemy.orm import Session
from app.db.models import Role, Permission
from app.schemas.role import RoleCreate, RoleUpdate
from fastapi import HTTPException

# Retrieve a role by ID
def get_role(db: Session, role_id: int):
    return db.query(Role).filter(Role.id == role_id).first()

# Retrieve a role by name
def get_role_by_name(db: Session, name: str):
    return db.query(Role).filter(Role.name == name).first()

# Retrieve all roles with pagination (skip and limit)
def get_roles(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Role).offset(skip).limit(limit).all()

# Create a new role
def create_role(db: Session, role_create: RoleCreate) -> Role:
    existing_role = get_role_by_name(db, role_create.name)
    if existing_role:
        raise HTTPException(status_code=400, detail=f"Role '{role_create.name}' already exists")
    
    new_role = Role(name=role_create.name)
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role

# Update an existing role by ID
def update_role(db: Session, role_id: int, role: RoleUpdate):
    db_role = get_role(db, role_id)
    if not db_role:
        raise HTTPException(status_code=404, detail="Role not found")

    if role.name:
        db_role.name = role.name

    db.commit()
    db.refresh(db_role)
    return db_role

# Delete a role by ID
def delete_role(db: Session, role_id: int):
    db_role = get_role(db, role_id)
    if not db_role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    db.delete(db_role)
    db.commit()
    return db_role

# Get all permissions associated with a role by role ID
def get_permissions_for_role(role_ids: list, db: Session):
    # Fetch permissions for the given role IDs using ANY for UUID arrays
    permissions_query = db.query(Permission).join(Role.permissions).filter(Role.id.in_(role_ids))
    permissions = permissions_query.all()
    return [permission.name for permission in permissions]


def assign_permission_to_role(db: Session, role_id: UUID, permission_id: UUID):
    # Fetch role and permission from the database
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    permission = db.query(Permission).filter(Permission.id == permission_id).first()
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")

    # Ensure permission is not already assigned
    if permission in role.permissions:
        raise HTTPException(status_code=400, detail="Permission already assigned to this role")

    # Assign permission to role
    role.permissions.append(permission)
    db.commit()
    db.refresh(role)
    
    return role

