from typing import TypeVar
from pathlib import Path

import yaml
from pydantic import BaseModel
from nonebot.params import Depends
from nonebot_plugin_uninfo import Uninfo

from .file import _get_index, _update_index, _get_session_config_file
from .config import global_config, plugin_config


class BaseSessionConfig(BaseModel):
    """
    会话配置基类

    所有会话配置类都应该继承此类，以便使用依赖注入功能。
    """

    pass


C = TypeVar("C", bound=BaseSessionConfig)


def _load_config(config_path: Path, config_type: type[C]):
    if not config_path.parent.exists():
        config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.touch()

    with config_path.open(encoding="utf-8") as rf:
        data = yaml.safe_load(rf)
    if not isinstance(data, dict):
        data = {}

    if plugin_config.session_config_use_global:
        for key, value in global_config.model_dump().items():
            data.setdefault(key, value)

    return config_type.model_validate(data)


def get_session_config(config_type: type[C]):
    """
    获取会话配置依赖项。

    用法：
        ```python
        from nonebot_plugin_session_config import BaseSessionConfig, get_session_config

        class SessionConfig(BaseSessionConfig):
            some_key: int = 0

        message_handler = on_message(...)

        @message_handler.handle()
        async def _(session_config: SessionConfig = get_session_config(SessionConfig)):
            ...
        ```
    """

    async def get_config(session: Uninfo):
        config_path = _get_session_config_file(session)
        config = _load_config(config_path, config_type)
        try:
            await _update_index(session, config_path)
        except Exception:
            pass
        return config

    return Depends(get_config)


async def traverse_session_configs(bot_id: str, config_type: type[C]):
    """
    遍历指定机器人的所有会话配置。

    返回一个字典，键为 `(scene_type, scene_id)` 元组，值为对应的会话配置实例。
    """
    result: dict[tuple[str, str], C] = {}
    index = await _get_index(bot_id)
    for (scene_type, scene_id), config_path in index.items():
        config = _load_config(config_path, config_type)
        result[(scene_type, scene_id)] = config
    return result
