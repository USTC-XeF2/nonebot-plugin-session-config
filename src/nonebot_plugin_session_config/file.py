import json
import asyncio
from pathlib import Path
from collections import defaultdict

from nonebot_plugin_uninfo import Uninfo
from nonebot_plugin_localstore import get_plugin_config_dir

from .config import plugin_config

PLUGIN_CONFIG_DIR = get_plugin_config_dir()


def _get_session_config_dir(bot_id: str):
    if plugin_config.session_config_base_dir is None:
        base_dir = PLUGIN_CONFIG_DIR
    else:
        base_dir = Path(plugin_config.session_config_base_dir)
    return base_dir / plugin_config.session_config_dir_format.format(bot_id=bot_id)


def _get_session_config_file(session: Uninfo):
    return _get_session_config_dir(
        session.self_id
    ) / plugin_config.session_config_file_format.format(
        scene_type=session.scene.type.name.lower(),
        scene_id=session.scene.id,
    )


_index_locks: dict[str, asyncio.Lock] = defaultdict(asyncio.Lock)


async def _update_index(session: Uninfo, config_path: Path):
    async with _index_locks[session.self_id]:
        index_file = _get_session_config_dir(session.self_id) / "index.json"
        if not index_file.parent.exists():
            index_file.parent.mkdir(parents=True, exist_ok=True)
        try:
            if index_file.exists():
                with index_file.open(encoding="utf-8") as rf:
                    data = json.load(rf)
            else:
                data = {}
        except Exception:
            data = {}

        key = f"{session.scene.type.name.lower()}:{session.scene.id}"
        data[key] = str(config_path)

        with index_file.open("w", encoding="utf-8") as wf:
            json.dump(data, wf, ensure_ascii=False, indent=2)


async def _get_index(bot_id: str) -> dict[tuple[str, str], Path]:
    async with _index_locks[bot_id]:
        index_file = _get_session_config_dir(bot_id) / "index.json"
        if index_file.exists():
            with index_file.open(encoding="utf-8") as rf:
                data = json.load(rf)
            return {tuple(k.split(":")): Path(v) for k, v in data.items()}
        else:
            return {}
