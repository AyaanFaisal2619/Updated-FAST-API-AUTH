import uuid
from sqlalchemy import UUID, Column, DateTime, Integer, String, ForeignKey, Table, Boolean
from sqlalchemy.orm import relationship
from .session import Base

# Many-to-many relationship between Role and Permission
role_permissions_table = Table(
    'role_permissions', Base.metadata,
    Column('role_id', UUID(as_uuid=True), ForeignKey('roles.id'), primary_key=True),
    Column('permission_id', UUID(as_uuid=True), ForeignKey('permissions.id'), primary_key=True)
)

user_roles_table = Table(
    'user_roles', Base.metadata,
    Column('user_id', UUID(as_uuid=True), ForeignKey('users.id'), primary_key=True),
    Column('role_id', UUID(as_uuid=True), ForeignKey('roles.id'), primary_key=True)
)


class User(Base):
    __tablename__ = 'users'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    # Many-to-many relationship with Role
    roles = relationship('Role', secondary=user_roles_table, back_populates='users')

class Role(Base):
    __tablename__ = 'roles'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)

    # Many-to-many relationships
    permissions = relationship('Permission', secondary=role_permissions_table, back_populates='roles')
    users = relationship('User', secondary=user_roles_table, back_populates='roles')

class Permission(Base):
    __tablename__ = 'permissions'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)

    # Many-to-many relationship with Role
    roles = relationship('Role', secondary=role_permissions_table, back_populates='permissions')
