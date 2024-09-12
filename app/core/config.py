from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = "a3f9f8b8d7e8f6c9a7b5c6d8f9e8b7a6"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # Token expiration time in minutes (1 Day)

    class Config:
        env_file = ".env"  # Load environment variables from .env file

settings = Settings()
