from typing import Any

from nonebot.params import DependParam
from nonebot.dependencies import Param


def inject_after(
    obj: Any,
    field_name: str,
    param: type[Param],
    after_param: type[Param] = DependParam,
):
    original_params = getattr(obj, field_name)

    if not (
        isinstance(original_params, (list, tuple))
        and all(issubclass(p, Param) for p in original_params)
    ):
        raise TypeError(f"{field_name} is not a list or tuple of Param subclasses")

    original_params_type = type(original_params)
    original_params_list: list[type[Param]] = list(original_params)

    for i, p in enumerate(original_params_list):
        if p is after_param:
            original_params_list.insert(i + 1, param)
            break
    else:
        original_params_list.append(param)

    setattr(obj, field_name, original_params_type(original_params_list))


def inject_all(param: type[Param], after_param: type[Param] = DependParam):
    import nonebot.message
    from nonebot.rule import Rule
    from nonebot.matcher import Matcher
    from nonebot.permission import Permission

    inject_list = [
        (nonebot.message, "EVENT_PCS_PARAMS"),
        (nonebot.message, "RUN_PREPCS_PARAMS"),
        (nonebot.message, "RUN_POSTPCS_PARAMS"),
        (Rule, "HANDLER_PARAM_TYPES"),
        (Matcher, "HANDLER_PARAM_TYPES"),
        (Permission, "HANDLER_PARAM_TYPES"),
    ]

    for obj, field_name in inject_list:
        inject_after(obj, field_name, param, after_param=after_param)
