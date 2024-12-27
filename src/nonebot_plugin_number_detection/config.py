from pydantic import BaseModel
from nonebot import get_plugin_config

class Config(BaseModel):
    is_automatic: bool = False
    headcount: int = 10

plugin_config = get_plugin_config(config= Config)