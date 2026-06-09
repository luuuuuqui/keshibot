from __future__ import annotations

from typing import Any


def has_group_status_message(web_message: dict[str, Any]) -> bool:
    message = (web_message or {}).get("message") or {}
    if message.get("groupStatusMentionMessage"):
        return True
    text = str(message.get("conversation") or "")
    extended = str(message.get("extendedTextMessage", {}).get("text") or "")
    return "@status" in text.lower() or "@status" in extended.lower()
