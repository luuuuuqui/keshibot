from __future__ import annotations

import random
import re
import string
import unicodedata
from pathlib import Path
from typing import Any, TypedDict, cast

from takeshi_bot import config


JsonDict = dict[str, Any]


class ExtractedMessageData(TypedDict):
    args: list[str]
    command_name: str
    full_args: str
    full_message: str
    is_reply: bool
    prefix: str
    remote_jid: str | None
    reply_lid: str | None
    reply_text: str
    user_lid: str


def as_dict(value: Any) -> JsonDict:
    return cast(JsonDict, value) if isinstance(value, dict) else {}


def as_list(value: Any) -> list[Any]:
    return cast(list[Any], value) if isinstance(value, list) else []


def as_str(value: Any) -> str:
    return value if isinstance(value, str) else ""


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
    message = as_dict(web_message.get("message"))
    direct = message.get(f"{context}Message")
    if isinstance(direct, dict):
        return as_dict(direct)

    quoted = as_dict(
        as_dict(as_dict(message.get("extendedTextMessage")).get("contextInfo")).get(
            "quotedMessage"
        )
    )
    quoted_direct = quoted.get(f"{context}Message")
    if isinstance(quoted_direct, dict):
        return as_dict(quoted_direct)

    view_once = as_dict(as_dict(message.get("viewOnceMessage")).get("message"))
    view_once_direct = view_once.get(f"{context}Message")
    if isinstance(view_once_direct, dict):
        return as_dict(view_once_direct)

    quoted_view_once = as_dict(as_dict(quoted.get("viewOnceMessage")).get("message"))
    quoted_view_once_direct = quoted_view_once.get(f"{context}Message")
    if isinstance(quoted_view_once_direct, dict):
        return as_dict(quoted_view_once_direct)

    view_once_v2 = as_dict(as_dict(message.get("viewOnceMessageV2")).get("message"))
    view_once_v2_direct = view_once_v2.get(f"{context}Message")
    if isinstance(view_once_v2_direct, dict):
        return as_dict(view_once_v2_direct)

    quoted_view_once_v2 = as_dict(as_dict(quoted.get("viewOnceMessageV2")).get("message"))
    quoted_view_once_v2_direct = quoted_view_once_v2.get(f"{context}Message")
    return as_dict(quoted_view_once_v2_direct) if isinstance(quoted_view_once_v2_direct, dict) else None


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
    if not isinstance(params, dict):
        return None
    params_data = as_dict(params)
    for key in ("id", "selectedId", "selectedRowId", "rowId", "buttonId", "button_id"):
        value = params_data.get(key)
        if isinstance(value, str) and value:
            return value
    return None


def extract_data_from_message(web_message: dict[str, Any]) -> ExtractedMessageData:
    message = as_dict(web_message.get("message"))
    extended = as_dict(message.get("extendedTextMessage"))
    image_message = as_dict(message.get("imageMessage"))
    video_message = as_dict(message.get("videoMessage"))
    buttons_response = as_dict(message.get("buttonsResponseMessage"))
    template_button_reply = as_dict(message.get("templateButtonReplyMessage"))
    list_response = as_dict(message.get("listResponseMessage"))
    single_select_reply = as_dict(list_response.get("singleSelectReply"))
    interactive = as_dict(
        as_dict(message.get("interactiveResponseMessage")).get(
            "nativeFlowResponseMessage"
        )
    )

    full_message = as_str(
        message.get("conversation")
        or extended.get("text")
        or image_message.get("caption")
        or video_message.get("caption")
        or buttons_response.get("selectedButtonId")
        or template_button_reply.get("selectedId")
        or single_select_reply.get("selectedRowId")
        or _extract_interactive_response_id(as_str(interactive.get("paramsJson")))
        or "#auto-command"
    )

    context_info = as_dict(extended.get("contextInfo"))
    quoted = as_dict(context_info.get("quotedMessage"))
    is_reply = bool(extended and quoted)
    reply_text = as_str(
        quoted.get("conversation")
        or as_dict(quoted.get("extendedTextMessage")).get("text")
        or as_dict(quoted.get("imageMessage")).get("caption")
        or ""
    )

    key = as_dict(web_message.get("key"))
    participant = as_str(key.get("participant"))
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
        "remote_jid": cast(str | None, key.get("remoteJid")),
        "reply_lid": cast(str | None, context_info.get("participant")),
        "reply_text": reply_text,
        "user_lid": user_lid,
    }


def remove_file_if_exists(file_path: str | Path | None) -> None:
    if file_path is None:
        return
    path = Path(file_path)
    if path.exists():
        path.unlink()
