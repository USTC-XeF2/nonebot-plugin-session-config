from nonebot import get_driver, get_plugin_config
from pydantic import BaseModel


class Config(BaseModel):
    session_config_base_dir: str | None = None
    session_config_dir_format: str = "bot-{bot_id}"
    session_config_file_format: str = "{scene_type}-{scene_id}.yaml"
    session_config_use_global: bool = False


plugin_config = get_plugin_config(Config)
global_config = get_driver().config
