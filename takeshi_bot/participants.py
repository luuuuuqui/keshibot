from __future__ import annotations

from takeshi_bot.bridge import BaileysBridge
from takeshi_bot.database import (
    is_active_exit_group,
    is_active_group,
    is_active_welcome_group,
)
from takeshi_bot.messages import exit_message, welcome_message
from takeshi_bot.utils import only_numbers


def extract_user_lid(data: str | list[str] | None) -> str:
    if isinstance(data, list):
        return data[0] if data else ""
    return data or ""


async def on_group_participants_update(
    bridge: BaileysBridge, remote_jid: str, data: str | list[str], action: str
) -> None:
    if not remote_jid.endswith("@g.us") or not is_active_group(remote_jid):
        return

    user_lid = extract_user_lid(data)
    if not user_lid:
        return

    if action == "add" and is_active_welcome_group(remote_jid):
        text = welcome_message
    elif action == "remove" and is_active_exit_group(remote_jid):
        text = exit_message
    else:
        return

    mentions: list[str] = []
    if "@member" in text:
        text = text.replace("@member", f"@{only_numbers(user_lid)}")
        mentions.append(user_lid)

    try:
        profile_image_url = await bridge.request(
            "profile_picture_url", {"jid": user_lid, "type": "image"}
        )
    except Exception:
        profile_image_url = None

    if profile_image_url:
        content: dict[str, object] = {
            "image": {"url": profile_image_url},
            "caption": text,
        }
    else:
        content = {"text": text}

    if mentions:
        content["mentions"] = mentions
    await bridge.send_message(remote_jid, content)
