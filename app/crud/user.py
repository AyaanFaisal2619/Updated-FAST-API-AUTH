import uuid
from fastapi import HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from app.core.security import get_password_hash
from app.db.models import User, Role
from app.schemas.user import UserCreate, UserUpdate


def create_user(db: Session, user_create: UserCreate) -> User:
    # Hash the password before storing it
    hashed_password = get_password_hash(user_create.password)
    
    db_user = User(
        username=user_create.username,
        email=user_create.email.strip(),
        password_hash=hashed_password,  # Store the hashed password
        is_active=user_create.is_active
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: UUID) -> User:
    return db.query(User).filter(User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 10) -> list[User]:
    return db.query(User).offset(skip).limit(limit).all()

def get_user_by_email(db: Session , email :str):
    return db.query(User).filter(User.email == email.strip()).first()

def get_user_by_username(db: Session, name :str):
    return db.query(User).filter(User.username == name).first()

def update_user(db: Session, user_id: UUID, user_update: UserUpdate) -> User:
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        if user_update.username:
            db_user.username = user_update.username
        if user_update.email:
            db_user.email = user_update.email
        if user_update.password:
            db_user.password_hash = user_update.password  # Assuming you handle password hashing elsewhere
        if user_update.is_active is not None:
            db_user.is_active = user_update.is_active
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: UUID) -> None:
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()

def assign_role_to_user(db: Session, user_id: str, role_id: str):
    user = db.query(User).filter(User.id == user_id).first()
    role = db.query(Role).filter(Role.id == role_id).first()
    
    # Check if the role is already assigned
    if role in user.roles:
        return {"message": f"Role '{role.name}' is already assigned to user '{user.username}'"}
    
    # Add the role if not already assigned
    user.roles.append(role)
    db.commit()
    return {"message": f"Role '{role.name}' assigned to user '{user.username}' successfully"}
