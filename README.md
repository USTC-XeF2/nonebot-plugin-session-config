<div align="center">
    <a href="https://v2.nonebot.dev/store">
    <img src="https://raw.githubusercontent.com/fllesser/nonebot-plugin-template/refs/heads/resource/.docs/NoneBotPlugin.svg" width="310" alt="logo"></a>

## ✨ nonebot-plugin-session-config ✨
[![LICENSE](https://img.shields.io/github/license/USTC-XeF2/nonebot-plugin-session-config.svg)](./LICENSE)
[![pypi](https://img.shields.io/pypi/v/nonebot-plugin-session-config.svg)](https://pypi.python.org/pypi/nonebot-plugin-session-config)
[![python](https://img.shields.io/badge/python-3.10|3.11|3.12|3.13-blue.svg)](https://www.python.org)
[![uv](https://img.shields.io/badge/package%20manager-uv-black?style=flat-square&logo=uv)](https://github.com/astral-sh/uv)
<br/>
[![ruff](https://img.shields.io/badge/code%20style-ruff-black?style=flat-square&logo=ruff)](https://github.com/astral-sh/ruff)
[![pre-commit](https://results.pre-commit.ci/badge/github/USTC-XeF2/nonebot-plugin-session-config/master.svg)](https://results.pre-commit.ci/latest/github/USTC-XeF2/nonebot-plugin-session-config/master)

</div>

## 📖 介绍

本插件为每个会话（群聊、私聊等场景）提供了独立的持久化配置存储功能。

## 💿 安装

### 使用 nb-cli 安装

```shell
nb plugin install nonebot-plugin-session-config --upgrade
```

### 使用 uv 安装

```shell
uv add nonebot-plugin-session-config
```

安装仓库 master 分支

```shell
uv add git+https://github.com/USTC-XeF2/nonebot-plugin-session-config@master
```

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot.plugins]` 部分追加写入

```toml
"@local" = ["nonebot_plugin_session_config"]
```

## ⚙️ 配置

所有配置项均以 `SESSION_CONFIG_` 为前缀（下文省略），且均为选填项。

| 配置项 | 默认值 | 说明 |
| :---: | :---: | :-: |
| BASE_DIR | None | 配置存储的根目录，值为 None 时使用 `localstore` 提供的配置文件目录，**一般不需要更改** |
| DIR_FORMAT | bot-{bot_id} | 各机器人所属目录的命名格式，不使用 `bot_id` 模板参数时所有机器人共用同一目录 |
| FILE_FORMAT | {scene_type}-{scene_id}.yaml | 配置文件的命名格式 |
| USE_GLOBAL | False | 是否尝试使用全局配置作为默认值，**开启此项时请确保会话配置与全局配置间没有意料外的重复键** |
| ENABLE_PARAM | False | 是否启用会话配置参数注入功能，启用后可直接指定会话配置类作为消息处理函数参数类型，**在插件冲突时可能会注入失败** |

## 🎉 使用

```python
from nonebot import on_message

from nonebot_plugin_session_config import (
    BaseSessionConfig,
    check_enabled,
    get_session_config,
)


# 所有会话配置类均应继承自 BaseSessionConfig
class SessionConfig(BaseSessionConfig):
    test_enabled: bool = False
    test_key: int = 0


message_handler = on_message(
    rule=check_enabled(SessionConfig, "test_enabled"),
)


@message_handler.handle()
async def _(session_config: SessionConfig = get_session_config(SessionConfig)):
    await message_handler.finish(f"Test key value is: {session_config.test_key}")


# 使用自动参数注入（需在配置中启用 ENABLE_PARAM 选项）
@message_handler.handle()
async def _(session_config: SessionConfig):
    await message_handler.finish(f"Test key value is: {session_config.test_key}")
```

本插件提供的配置不提供在程序中动态修改的接口，若需要修改请手动或自动编辑对应的文件，无需重启即可更新。
