from pydantic_settings import BaseSettings
from src.utils.singleton import singleton
import os

# Global App settings, can be changed by environment variables(.env.local)
@singleton
class Settings(BaseSettings):
    allowed_origins: list[str]
    hf_token: str
    models_cache_dir: str
    
    class Config:
      env_file = ".env.local"
      case_sensitive = False