from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    groq_api_key: str
    environment: str = "development"
    app_name: str = "AI Text Intelligence API"
    app_version: str = "1.0.0"
    
    # Model settings
    groq_model: str = "openai/gpt-oss-120b"
    max_tokens: int = 1024
    temperature: float = 0.7
    
    class Config:
        env_file = ".env"
        case_sensitive = False

@lru_cache()
def get_settings():
    return Settings()