import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Nexra Intelligence API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Database
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "nexra")
    
    # AI Integration
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
    @property
    def ASYNC_DATABASE_URI(self) -> str:
        # Vercel and Render inject the full URL as POSTGRES_URL or DATABASE_URL
        direct_url = os.getenv("POSTGRES_URL") or os.getenv("DATABASE_URL")
        if direct_url:
            # SQLAlchemy asyncpg requires postgresql+asyncpg://
            if direct_url.startswith("postgres://"):
                direct_url = direct_url.replace("postgres://", "postgresql+asyncpg://", 1)
            elif direct_url.startswith("postgresql://"):
                direct_url = direct_url.replace("postgresql://", "postgresql+asyncpg://", 1)
            return direct_url
            
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

settings = Settings()
