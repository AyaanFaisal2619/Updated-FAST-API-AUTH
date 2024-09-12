from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import users, roles, permissions, roles_permissions
from app.db.session import Base, engine

app = FastAPI()

# Create the database tables
Base.metadata.create_all(bind=engine)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Add frontend origins here
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


# Register the routers with correct prefixes and tags
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(roles.router, prefix="/roles", tags=["roles"])
app.include_router(permissions.router, prefix="/permissions", tags=["permissions"])
app.include_router(roles_permissions.router, prefix="/roles_permissions", tags=["roles_permissions"])

