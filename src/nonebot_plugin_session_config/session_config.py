from typing import TYPE_CHECKING, TypeVar, Annotated
from pathlib import Path

import yaml
from pydantic import BaseModel
from nonebot.params import Depends
from nonebot_plugin_uninfo import Uninfo
from nonebot_plugin_localstore import get_plugin_config_dir

from .config import global_config, plugin_config

PLUGIN_CONFIG_DIR = get_plugin_config_dir()


def _get_session_config_dir(bot_id: str):
    if plugin_config.session_config_base_dir is None:
        base_dir = PLUGIN_CONFIG_DIR
    else:
        base_dir = Path(plugin_config.session_config_base_dir)
    return base_dir / plugin_config.session_config_dir_format.format(bot_id=bot_id)


C = TypeVar("C", bound=BaseModel)


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
        from nonebot_plugin_session_config import SessConfig, get_session_config
        from pydantic import BaseModel

        class Config(BaseModel):
            some_key: int = 0

        message_handler = on_message(...)

        @message_handler.handle()
        async def _(session_config: Config = get_session_config(Config)):
            ...

        # 也可以写作
        @message_handler.handle()
        async def _(session_config: SessConfig[Config]):
            ...
        ```
    """

    def get_config(session: Uninfo):
        config_path = _get_session_config_dir(
            session.self_id
        ) / plugin_config.session_config_file_format.format(
            scene_type=session.scene.type.name.lower(),
            scene_id=session.scene.id,
        )
        return _load_config(config_path, config_type)

    return Depends(get_config)


if TYPE_CHECKING:
    SessConfig = C
else:

    class SessConfig:
        def __class_getitem__(cls, model_type: type[C]):
            return Annotated[model_type, get_session_config(model_type)]
