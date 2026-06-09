from __future__ import annotations

from typing import Any

MAX_PAYMENT_SCAN_DEPTH = 8
PAYMENT_MESSAGE_KEYS = {"requestPaymentMessage"}


def _can_scan(value: Any) -> bool:
    return isinstance(value, dict)


def _has_payment_key(value: Any, depth: int = 0, seen: set[int] | None = None) -> bool:
    if seen is None:
        seen = set()
    if not _can_scan(value) or depth > MAX_PAYMENT_SCAN_DEPTH:
        return False
    object_id = id(value)
    if object_id in seen:
        return False
    seen.add(object_id)

    for key, child in value.items():
        if key == "quotedMessage":
            continue
        if key in PAYMENT_MESSAGE_KEYS and _can_scan(child):
            return True
        if _has_payment_key(child, depth + 1, seen):
            return True
    return False


def has_payment_message(web_message: dict[str, Any]) -> bool:
    return _has_payment_key((web_message or {}).get("message"))
