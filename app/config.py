from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict
from pathlib import Path
import os

os.environ["CQLENG_ALLOW_SCHEMA_MANAGEMENT"] = "1"

class Settings(BaseSettings):
    base_dir: Path = Path(__file__).resolve().parent
    templates_dir: Path = Path(__file__).resolve().parent / "templates"
    keyspace: str = Field(..., alias="ASTRADB_KEYSPACE")
    secret_key: str = Field(...)
    jwt_algo: str = Field(default="HS256")
    model_config = ConfigDict(env_file=".env")

    # class Config:
    #     env_file = ".env"

@lru_cache
def get_settings():
    return Settings()