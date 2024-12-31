from pydantic import BaseModel
from nonebot import get_plugin_config

class Config(BaseModel):
    detect_is_automatic: bool = False
    detect_headcount: int = 10

plugin_config = get_plugin_config(config= Config)