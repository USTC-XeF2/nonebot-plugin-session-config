import inspect
from typing import Any
from typing_extensions import override

from nonebot.utils import generic_check_issubclass
from nonebot.adapters import Bot, Event
from nonebot.dependencies import Param
from nonebot_plugin_uninfo import get_session

from .session_config import BaseSessionConfig, _load_config, _get_session_config_file


class SessionConfigParam(Param):
    def __init__(
        self,
        *args,
        config_type: type[BaseSessionConfig] | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.config_type = config_type

    def __repr__(self) -> str:
        return f"SessionConfigParam({self.config_type!r})"

    @classmethod
    @override
    def _check_param(
        cls, param: inspect.Parameter, allow_types: tuple[type[Param], ...]
    ):
        if generic_check_issubclass(param.annotation, BaseSessionConfig):
            return cls(config_type=param.annotation)

    @override
    async def _solve(  # pyright: ignore[reportIncompatibleMethodOverride]
        self, bot: Bot, event: Event, **kwargs: Any
    ):
        session = await get_session(bot, event)
        if session is None:
            raise ValueError("No session available for SessionConfigParam")
        if self.config_type is None:
            raise ValueError("SessionConfigParam requires a specific config type")

        config_path = _get_session_config_file(session)
        return _load_config(config_path, self.config_type)
