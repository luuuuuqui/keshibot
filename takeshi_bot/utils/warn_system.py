from __future__ import annotations

import time
from typing import Any

from takeshi_bot.database import WARNS_FILE, read_json, write_json

INITIAL_WARN_LIMIT = 3


def _load_db() -> dict[str, Any]:
    data = read_json(WARNS_FILE, {})
    if isinstance(data, list):
        return {}
    return data


def _save_db(data: dict[str, Any]) -> None:
    write_json(WARNS_FILE, data)


def _ensure_group(db: dict[str, Any], group_id: str) -> dict[str, Any]:
    return db.setdefault(group_id, {"warnLimit": INITIAL_WARN_LIMIT, "warns": {}})


def _ensure_user(db: dict[str, Any], group_id: str, user_lid: str) -> list[dict[str, Any]]:
    group = _ensure_group(db, group_id)
    return group.setdefault("warns", {}).setdefault(user_lid, [])


def add_warn(group_id: str, user_lid: str, reason: str = "Advertencia generica") -> int:
    db = _load_db()
    user = _ensure_user(db, group_id, user_lid)
    user.append({"reason": reason, "timestamp": int(time.time() * 1000), "valid": True})
    _save_db(db)
    return len([warn for warn in user if warn.get("valid")])


def get_all_warns(group_id: str, user_lid: str) -> list[dict[str, Any]]:
    db = _load_db()
    return db.get(group_id, {}).get("warns", {}).get(user_lid, [])


def get_warn_limit(group_id: str) -> int:
    db = _load_db()
    return int(db.get(group_id, {}).get("warnLimit", INITIAL_WARN_LIMIT))


def remove_last_warn(group_id: str, user_lid: str) -> int:
    db = _load_db()
    user = db.get(group_id, {}).get("warns", {}).get(user_lid)
    if not user:
        return 0
    for warn in reversed(user):
        if warn.get("valid"):
            warn["valid"] = False
            break
    _save_db(db)
    return len([warn for warn in user if warn.get("valid")])


def reactivate_warn_by_index(group_id: str, user_lid: str, index: int) -> bool:
    db = _load_db()
    user = db.get(group_id, {}).get("warns", {}).get(user_lid)
    if not user:
        return False
    invalid = [warn for warn in user if not warn.get("valid")]
    if index < 0 or index >= len(invalid):
        return False
    target = invalid[index]
    target["valid"] = True
    _save_db(db)
    return True
