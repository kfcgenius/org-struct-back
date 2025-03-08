from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class NodeSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="OSB_NODE_")
    min_depth: int = Field(default=1)
    max_depth: int = Field(default=100)
