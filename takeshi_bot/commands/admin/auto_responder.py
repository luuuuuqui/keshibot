from __future__ import annotations

from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext
from takeshi_bot.database import (
    activate_auto_responder_group,
    deactivate_auto_responder_group,
)
from takeshi_bot.errors import InvalidParameterError
from takeshi_bot.utils import is_false, is_true


async def handle(ctx: CommandContext) -> None:
    value = ctx.args[0] if ctx.args else ctx.full_args.strip()
    if is_true(value):
        activate_auto_responder_group(ctx.remote_jid)
        await ctx.send_success_reply("Auto-responder ativado!")
    elif is_false(value):
        deactivate_auto_responder_group(ctx.remote_jid)
        await ctx.send_success_reply("Auto-responder desativado!")
    else:
        raise InvalidParameterError("Use on/off.")


command = Command(
    name="auto-responder",
    description="Ativa ou desativa respostas automaticas.",
    commands=["auto-responder", "autoresponder"],
    usage="/auto-responder on",
    handle=handle,
)
