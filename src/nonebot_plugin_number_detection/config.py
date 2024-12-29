from pydantic import BaseModel
from nonebot import get_plugin_config

class Config(BaseModel):
    examine_is_automatic: bool = False
    examine_headcount: int = 10

plugin_config = get_plugin_config(config= Config)