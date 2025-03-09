from pydantic import BaseModel
from nonebot import get_plugin_config

class Config(BaseModel):
    detect_headcount: int = 5
    detect_is_automatic: bool = False
    
    class Config:
        extra = "ignore"


plugin_config = get_plugin_config(config= Config)