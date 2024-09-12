# app/core/permissions.py
from fastapi import Depends, HTTPException, status
from app.api.deps import get_current_user
from app.crud.roles import get_permissions_for_role
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import User

def require_permission(permission: str):
    def permission_dependency(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
        # Extract role IDs from user.roles
        role_ids = [role.id for role in user.roles]
        
        # Get permissions for these role IDs
        permissions = get_permissions_for_role(role_ids, db)
        
        if permission not in permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail=f"User does not have the '{permission}' permission"
            )
        return user
    return permission_dependency
