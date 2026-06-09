from __future__ import annotations

import json
import os
from copy import deepcopy
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Any

from . import config
from .paths import DATABASE_DIR

ANTI_LINK_GROUPS_FILE = "anti-link-groups"
AUTO_RESPONDER_FILE = "auto-responder"
AUTO_RESPONDER_GROUPS_FILE = "auto-responder-groups"
AUTO_STICKER_GROUPS_FILE = "auto-sticker-groups"
CONFIG_FILE = "config"
EXIT_GROUPS_FILE = "exit-groups"
GROUP_RESTRICTIONS_FILE = "group-restrictions"
INACTIVE_GROUPS_FILE = "inactive-groups"
MUTE_FILE = "muted"
ONLY_ADMINS_FILE = "only-admins"
PREFIX_GROUPS_FILE = "prefix-groups"
RESTRICTED_MESSAGES_FILE = "restricted-messages"
WELCOME_GROUPS_FILE = "welcome-groups"
WARNS_FILE = "warns"


def _path(name: str) -> Path:
    return DATABASE_DIR / f"{name}.json"


def _clone(value: Any) -> Any:
    return deepcopy(value)


def read_json(name: str, default: Any | None = None) -> Any:
    if default is None:
        default = []
    DATABASE_DIR.mkdir(parents=True, exist_ok=True)
    path = _path(name)
    if not path.exists():
        write_json(name, default)
        return _clone(default)
    with path.open("r", encoding="utf-8") as file:
        content = file.read().strip()
    if not content:
        return _clone(default)
    return json.loads(content)


def write_json(name: str, data: Any) -> None:
    DATABASE_DIR.mkdir(parents=True, exist_ok=True)
    path = _path(name)
    with NamedTemporaryFile(
        "w", encoding="utf-8", delete=False, dir=DATABASE_DIR, suffix=".tmp"
    ) as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
        file.write("\n")
        temp_name = file.name
    os.replace(temp_name, path)


def _activate_list_item(filename: str, value: str) -> None:
    items = read_json(filename)
    if value not in items:
        items.append(value)
        write_json(filename, items)


def _deactivate_list_item(filename: str, value: str) -> None:
    items = read_json(filename)
    if value in items:
        items.remove(value)
        write_json(filename, items)


def _contains(filename: str, value: str) -> bool:
    return value in read_json(filename)


def activate_exit_group(group_id: str) -> None:
    _activate_list_item(EXIT_GROUPS_FILE, group_id)


def deactivate_exit_group(group_id: str) -> None:
    _deactivate_list_item(EXIT_GROUPS_FILE, group_id)


def is_active_exit_group(group_id: str) -> bool:
    return _contains(EXIT_GROUPS_FILE, group_id)


def activate_welcome_group(group_id: str) -> None:
    _activate_list_item(WELCOME_GROUPS_FILE, group_id)


def deactivate_welcome_group(group_id: str) -> None:
    _deactivate_list_item(WELCOME_GROUPS_FILE, group_id)


def is_active_welcome_group(group_id: str) -> bool:
    return _contains(WELCOME_GROUPS_FILE, group_id)


def activate_group(group_id: str) -> None:
    _deactivate_list_item(INACTIVE_GROUPS_FILE, group_id)


def deactivate_group(group_id: str) -> None:
    _activate_list_item(INACTIVE_GROUPS_FILE, group_id)


def is_active_group(group_id: str) -> bool:
    return not _contains(INACTIVE_GROUPS_FILE, group_id)


def get_auto_responder_response(match: str) -> str | None:
    responses = read_json(AUTO_RESPONDER_FILE)
    match_upper = match.upper()
    for response in responses:
        if str(response.get("match", "")).upper() == match_upper:
            return response.get("answer")
    return None


def activate_auto_responder_group(group_id: str) -> None:
    _activate_list_item(AUTO_RESPONDER_GROUPS_FILE, group_id)


def deactivate_auto_responder_group(group_id: str) -> None:
    _deactivate_list_item(AUTO_RESPONDER_GROUPS_FILE, group_id)


def is_active_auto_responder_group(group_id: str) -> bool:
    return _contains(AUTO_RESPONDER_GROUPS_FILE, group_id)


def activate_anti_link_group(group_id: str) -> None:
    _activate_list_item(ANTI_LINK_GROUPS_FILE, group_id)


def deactivate_anti_link_group(group_id: str) -> None:
    _deactivate_list_item(ANTI_LINK_GROUPS_FILE, group_id)


def is_active_anti_link_group(group_id: str) -> bool:
    return _contains(ANTI_LINK_GROUPS_FILE, group_id)


def activate_auto_sticker_group(group_id: str) -> None:
    _activate_list_item(AUTO_STICKER_GROUPS_FILE, group_id)


def deactivate_auto_sticker_group(group_id: str) -> None:
    _deactivate_list_item(AUTO_STICKER_GROUPS_FILE, group_id)


def is_active_auto_sticker_group(group_id: str) -> bool:
    return _contains(AUTO_STICKER_GROUPS_FILE, group_id)


def mute_member(group_id: str, member_id: str) -> None:
    muted = read_json(MUTE_FILE, {})
    group_muted = muted.setdefault(group_id, [])
    if member_id not in group_muted:
        group_muted.append(member_id)
        write_json(MUTE_FILE, muted)


def unmute_member(group_id: str, member_id: str) -> None:
    muted = read_json(MUTE_FILE, {})
    group_muted = muted.get(group_id, [])
    if member_id in group_muted:
        group_muted.remove(member_id)
        write_json(MUTE_FILE, muted)


def check_if_member_is_muted(group_id: str | None, member_id: str | None) -> bool:
    if not group_id or not member_id:
        return False
    muted = read_json(MUTE_FILE, {})
    return member_id in muted.get(group_id, [])


def activate_only_admins(group_id: str) -> None:
    _activate_list_item(ONLY_ADMINS_FILE, group_id)


def deactivate_only_admins(group_id: str) -> None:
    _deactivate_list_item(ONLY_ADMINS_FILE, group_id)


def is_active_only_admins(group_id: str) -> bool:
    return _contains(ONLY_ADMINS_FILE, group_id)


def read_group_restrictions() -> dict[str, dict[str, bool]]:
    data = read_json(GROUP_RESTRICTIONS_FILE, {})
    if isinstance(data, list):
        converted: dict[str, dict[str, bool]] = {}
        for item in data:
            group_id = item.get("groupId")
            if group_id:
                converted[group_id] = {
                    key: bool(value)
                    for key, value in item.items()
                    if key != "groupId"
                }
        return converted
    return data


def save_group_restrictions(restrictions: dict[str, dict[str, bool]]) -> None:
    write_json(GROUP_RESTRICTIONS_FILE, restrictions)


def is_active_group_restriction(group_id: str, restriction: str) -> bool:
    restrictions = read_group_restrictions()
    return bool(restrictions.get(group_id, {}).get(restriction))


def update_is_active_group_restriction(
    group_id: str, restriction: str, is_active: bool
) -> None:
    restrictions = read_group_restrictions()
    target = restrictions.setdefault(group_id, {})
    target[restriction] = is_active
    save_group_restrictions(restrictions)


def read_restricted_message_types() -> list[dict[str, Any]]:
    return read_json(RESTRICTED_MESSAGES_FILE)


def set_prefix(group_jid: str, prefix: str) -> None:
    prefixes = read_json(PREFIX_GROUPS_FILE, {})
    prefixes[group_jid] = prefix
    write_json(PREFIX_GROUPS_FILE, prefixes)


def get_prefix(group_jid: str) -> str:
    prefixes = read_json(PREFIX_GROUPS_FILE, {})
    return prefixes.get(group_jid, config.PREFIX)


def list_auto_responder_items() -> list[dict[str, str]]:
    return read_json(AUTO_RESPONDER_FILE)


def add_auto_responder_item(match: str, answer: str) -> None:
    items = list_auto_responder_items()
    next_key = max([int(item.get("key", 0)) for item in items] or [0]) + 1
    items.append({"key": next_key, "match": match, "answer": answer})
    write_json(AUTO_RESPONDER_FILE, items)


def remove_auto_responder_item_by_key(key: int) -> bool:
    items = list_auto_responder_items()
    filtered = [item for item in items if int(item.get("key", 0)) != int(key)]
    if len(filtered) == len(items):
        return False
    write_json(AUTO_RESPONDER_FILE, filtered)
    return True


def set_spider_api_token(token: str) -> None:
    runtime_config = read_json(CONFIG_FILE, {})
    runtime_config["spider_api_token"] = token
    write_json(CONFIG_FILE, runtime_config)


def get_spider_api_token() -> str:
    runtime_config = read_json(CONFIG_FILE, {})
    return runtime_config.get("spider_api_token") or config.SPIDER_API_TOKEN
