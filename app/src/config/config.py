from pydantic_settings import BaseSettings
from src.utils.singleton import singleton


# Global App settings, can be changed by environment variables(.env)
class Settings(BaseSettings):
  SOME_TOKEN: str = ''

@singleton
class Config:
    def __init__(self):        
        self.app = Settings()
