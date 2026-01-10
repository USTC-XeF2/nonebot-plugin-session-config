from nonebot import require
from nonebot.plugin import PluginMetadata, inherit_supported_adapters

require("nonebot_plugin_uninfo")
require("nonebot_plugin_localstore")

from .rules import check_enabled, check_condition
from .config import Config
from .session_config import SessConfig, get_session_config

__all__ = [
    "SessConfig",
    "check_condition",
    "check_enabled",
    "get_session_config",
]

__plugin_meta__ = PluginMetadata(
    name="会话配置",
    description="会话级配置信息存储插件",
    usage="session_config: SessConfig[YourConfigModel]",
    type="library",
    homepage="https://github.com/USTC-XeF2/nonebot-plugin-session-config",
    config=Config,
    supported_adapters=inherit_supported_adapters("nonebot_plugin_uninfo"),
)
