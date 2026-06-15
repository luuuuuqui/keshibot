from __future__ import annotations

import re

from takeshi_bot import config
from takeshi_bot.context import CommandContext
from takeshi_bot.database import get_prefix
from takeshi_bot.utils import as_dict, as_list


def verify_prefix(prefix: str, group_jid: str) -> bool:
    return prefix == get_prefix(group_jid)


def has_type_and_command(command_type: str, command: object | None) -> bool:
    return bool(command_type and command)


def is_link(text: str) -> bool:
    return bool(re.search(r"https?://|www\.|chat\.whatsapp\.com", text or "", re.I))


def is_bot_owner(user_lid: str | None) -> bool:
    return bool(user_lid and user_lid == config.OWNER_LID)


async def is_admin(ctx: CommandContext, user_lid: str | None = None) -> bool:
    target_lid = user_lid or ctx.user_lid
    if not target_lid or not ctx.is_group:
        return False
    metadata = await ctx.bridge.group_metadata(ctx.remote_jid)
    participants = [as_dict(item) for item in as_list(metadata.get("participants"))]
    for participant in participants:
        jid = participant.get("id") or participant.get("lid") or participant.get("jid")
        if jid == target_lid and participant.get("admin"):
            return True
    return False


async def check_permission(command_type: str, ctx: CommandContext) -> bool:
    if command_type == "member":
        return True
    if command_type == "owner":
        return is_bot_owner(ctx.user_lid)
    if command_type == "admin":
        return await is_admin(ctx)
    return False
