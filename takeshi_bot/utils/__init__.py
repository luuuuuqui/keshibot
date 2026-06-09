from __future__ import annotations

import random
import re
import string
import unicodedata
from pathlib import Path
from typing import Any

from takeshi_bot import config


def only_numbers(text: str) -> str:
    return re.sub(r"[^0-9]", "", text or "")


def remove_accents_and_special_characters(text: str) -> str:
    if not text:
        return ""
    normalized = unicodedata.normalize("NFD", text)
    return "".join(char for char in normalized if unicodedata.category(char) != "Mn")


def only_letters_and_numbers(text: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]", "", text or "")


def format_command(text: str) -> str:
    return only_letters_and_numbers(
        remove_accents_and_special_characters((text or "").lower().strip())
    )


def split_by_characters(text: str, characters: list[str]) -> list[str]:
    if not text:
        return []
    pattern = "[" + "".join(re.escape(char) for char in characters) + "]"
    return [part.strip() for part in re.split(pattern, text) if part.strip()]


def is_group(remote_jid: str | None) -> bool:
    return bool(remote_jid and remote_jid.endswith("@g.us"))


def is_true(word: str | None) -> bool:
    value = remove_accents_and_special_characters((word or "").lower())
    return value in {"1", "ativar", "ligado", "ligar", "on", "sim", "true"}


def is_false(word: str | None) -> bool:
    value = remove_accents_and_special_characters((word or "").lower())
    return value in {"0", "desativar", "desligado", "desligar", "off", "nao", "false"}


def to_user_lid(value: str) -> str:
    return f"{only_numbers(value)}@lid"


def to_user_jid(value: str) -> str:
    return f"{only_numbers(value)}@s.whatsapp.net"


def random_name(extension: str) -> str:
    suffix = "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(12))
    return f"{suffix}.{extension}"


def get_nested_message(web_message: dict[str, Any], context: str) -> dict[str, Any] | None:
    message = web_message.get("message") or {}
    direct = message.get(f"{context}Message")
    if direct:
        return direct

    quoted = (
        message.get("extendedTextMessage", {})
        .get("contextInfo", {})
        .get("quotedMessage", {})
    )
    if quoted.get(f"{context}Message"):
        return quoted.get(f"{context}Message")

    view_once = message.get("viewOnceMessage", {}).get("message", {})
    if view_once.get(f"{context}Message"):
        return view_once.get(f"{context}Message")

    quoted_view_once = quoted.get("viewOnceMessage", {}).get("message", {})
    if quoted_view_once.get(f"{context}Message"):
        return quoted_view_once.get(f"{context}Message")

    view_once_v2 = message.get("viewOnceMessageV2", {}).get("message", {})
    if view_once_v2.get(f"{context}Message"):
        return view_once_v2.get(f"{context}Message")

    quoted_view_once_v2 = quoted.get("viewOnceMessageV2", {}).get("message", {})
    return quoted_view_once_v2.get(f"{context}Message")


def baileys_is(web_message: dict[str, Any], context: str) -> bool:
    return get_nested_message(web_message, context) is not None


def _extract_interactive_response_id(params_json: str | None) -> str | None:
    if not params_json:
        return None
    import json

    try:
        params = json.loads(params_json)
    except json.JSONDecodeError:
        return None
    for key in ("id", "selectedId", "selectedRowId", "rowId", "buttonId", "button_id"):
        if params.get(key):
            return params[key]
    return None


def extract_data_from_message(web_message: dict[str, Any]) -> dict[str, Any]:
    message = web_message.get("message") or {}
    extended = message.get("extendedTextMessage") or {}
    interactive = (
        message.get("interactiveResponseMessage", {})
        .get("nativeFlowResponseMessage", {})
    )

    full_message = (
        message.get("conversation")
        or extended.get("text")
        or message.get("imageMessage", {}).get("caption")
        or message.get("videoMessage", {}).get("caption")
        or message.get("buttonsResponseMessage", {}).get("selectedButtonId")
        or message.get("templateButtonReplyMessage", {}).get("selectedId")
        or message.get("listResponseMessage", {})
        .get("singleSelectReply", {})
        .get("selectedRowId")
        or _extract_interactive_response_id(interactive.get("paramsJson"))
        or "#auto-command"
    )

    context_info = extended.get("contextInfo") or {}
    quoted = context_info.get("quotedMessage") or {}
    is_reply = bool(extended and quoted)
    reply_text = (
        quoted.get("conversation")
        or quoted.get("extendedTextMessage", {}).get("text")
        or quoted.get("imageMessage", {}).get("caption")
        or ""
    )

    key = web_message.get("key") or {}
    participant = key.get("participant") or ""
    user_lid = re.sub(r":[0-9][0-9]|:[0-9]", "", participant)

    command, *args = full_message.split(" ")
    prefix = command[0] if command else ""
    command_without_prefix = re.sub(f"^[{re.escape(config.PREFIX)}]+", "", command)

    return {
        "args": split_by_characters(" ".join(args), ["\\", "|", "/"]),
        "command_name": format_command(command_without_prefix),
        "full_args": " ".join(args),
        "full_message": full_message,
        "is_reply": is_reply,
        "prefix": prefix,
        "remote_jid": key.get("remoteJid"),
        "reply_lid": context_info.get("participant"),
        "reply_text": reply_text,
        "user_lid": user_lid,
    }


def remove_file_if_exists(file_path: str | Path) -> None:
    path = Path(file_path)
    if path.exists():
        path.unlink()
