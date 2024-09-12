

from fastapi import APIRouter, Depends, HTTPException, status,Request
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List

from app.core.security import create_access_token, get_password_hash, verify_password, oauth2_scheme
from app.crud import user as user_crud

from jose import jwt
from app.crud.roles import create_role, get_role, get_role_by_name
from app.db.models import User
from app.schemas.role import RoleCreate
from app.schemas.user import UserCreate, UserUpdate, UserOut, UserBase
from app.api.deps import ALGORITHM, SECRET_KEY, get_db, get_current_user
from app.core.permissions import require_permission

router = APIRouter()


@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user_create: UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_username(db, user_create.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return user_crud.create_user(db, user_create)

@router.get("/", response_model=List[UserOut])
def get_all_users(db: Session = Depends(get_db)):
    return user_crud.get_users(db)


@router.get("/{user_id}", response_model=UserOut)
def read_user(
    user_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(require_permission("view_user")),
    token: str = Depends(oauth2_scheme)  # Ensure the token is required
):
    db_user = user_crud.get_user(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.put("/{user_id}", response_model=UserOut)
def update_user(user_id: str, user_data: UserUpdate, db: Session = Depends(get_db)):
    updated_user = user_crud.update_user(db, user_id=user_id, user=user_data)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.delete("/{user_id}", response_model=UserOut)
def delete_user(user_id: str, db: Session = Depends(get_db)):
    deleted_user = user_crud.delete_user(db, user_id=user_id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="User not found")
    return deleted_user

@router.post("/signup", response_model=UserOut)
async def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    # Hash the password before creation
    
    
    # Get or create the default 'User' role
    role = get_role_by_name(db, name="User")
    if role is None:
        role_create = RoleCreate(name="User")  # Assuming RoleCreate is a Pydantic model
        role = create_role(db, role_create)
    
    # Create the user
    new_user = user_crud.create_user(db, user_data)
    
    if new_user:
        # Assign the 'User' role to the new user
        user_crud.assign_role_to_user(db, new_user.id, role.id)
        return new_user
    
    raise HTTPException(status_code=400, detail="User already exists")

@router.post("/users/{user_id}/assign_role/{role_id}", response_model=dict)
async def assign_role_to_user_endpoint(user_id: str, role_id: str, db: Session = Depends(get_db)):
    db_user = user_crud.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_role = get_role(db, role_id=role_id)
    if not db_role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    # Call the function to assign the role, or return a message if it's already assigned
    result = user_crud.assign_role_to_user(db, user_id=db_user.id, role_id=db_role.id)
    return result



class Token(BaseModel):
    access_token: str
    token_type: str

class Login(BaseModel):
    email: str
    password: str

@router.post("/signin", response_model=Token)
async def signin(login: Login, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_email(db, email=login.email)
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Verify the password hash
    if not verify_password(login.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Create a JWT token
    access_token = create_access_token(data={"sub": db_user.email})
    
    return {"access_token": access_token, "token_type": "bearer"}


import redis
from datetime import datetime, timedelta

r = redis.Redis()

def blacklist_token(token: str, expires_at: int):
    # Store the token with an expiration time in Redis
    r.setex(token, expires_at - int(datetime.utcnow().timestamp()), "blacklisted")

def is_token_blacklisted(token: str) -> bool:
    return r.exists(token) == 1


@router.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    # Decode token to get expiry time
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    exp = payload.get("exp")
    if exp is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token")

    blacklist_token(token, exp)
    return {"msg": "Successfully logged out"}