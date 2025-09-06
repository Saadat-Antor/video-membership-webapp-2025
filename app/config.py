from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import Field
import os

os.environ["CQLENG_ALLOW_SCHEMA_MANAGEMENT"] = "1"

class Settings(BaseSettings):
    keyspace: str = Field(..., alias="ASTRADB_KEYSPACE")

    class Config:
        env_file = ".env"

@lru_cache
def get_settings():
    return Settings()