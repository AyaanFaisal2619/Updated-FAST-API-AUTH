from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud.roles import get_role_by_name, assign_permission_to_role
from app.crud.permissions import get_permission_by_name
from app.api.deps import get_db
from uuid import UUID

router = APIRouter()

@router.post("/roles/{role_name}/permissions/{permission_name}", response_model=dict)
async def assign_permission_to_role_endpoint(role_name: str, permission_name: str, db: Session = Depends(get_db)):
    # Retrieve role by name
    role = get_role_by_name(db, role_name)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    # Retrieve permission by name
    permission = get_permission_by_name(db, permission_name)
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    
    # Assign permission to role
    updated_role = assign_permission_to_role(db, role.id, permission.id)
    
    return {"message": f"Permission '{permission_name}' assigned to role '{role_name}' successfully"}
