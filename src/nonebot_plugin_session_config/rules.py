from collections.abc import Callable

from nonebot.rule import Rule

from .session_config import C, get_session_config


def check_condition(config_type: type[C], checker: Callable[[C], bool]):
    """
    创建一个基于会话配置的简单规则检查器。用于简化较为简单的条件判断，复杂条件请使用自定义依赖注入的规则函数。

    用法：
        ```python
        from nonebot_plugin_session_config import check_condition

        message_handler = on_message(
            ...,
            rule=check_condition(Config, lambda cfg: cfg.some_key > 0),
        )
        ```
    """

    def rule_checker(session_config: C = get_session_config(config_type)):
        return checker(session_config)

    return Rule(rule_checker)


def check_enabled(config_type: type[C], key: str):
    """
    创建一个基于会话配置中布尔值的规则检查器，具体用法见 `check_condition`。
    """
    if key not in config_type.model_fields:
        raise ValueError(f"Key '{key}' not found in config '{config_type.__name__}'")

    return check_condition(
        config_type,
        lambda session_config: getattr(session_config, key),
    )
