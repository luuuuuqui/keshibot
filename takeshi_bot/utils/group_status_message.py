from __future__ import annotations

from typing import Any

from takeshi_bot.utils import as_dict, as_str


def has_group_status_message(web_message: dict[str, Any]) -> bool:
    message = as_dict(web_message.get("message"))
    if message.get("groupStatusMentionMessage"):
        return True
    text = as_str(message.get("conversation"))
    extended = as_str(as_dict(message.get("extendedTextMessage")).get("text"))
    return "@status" in text.lower() or "@status" in extended.lower()
