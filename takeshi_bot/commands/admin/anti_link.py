from __future__ import annotations

from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext
from takeshi_bot.database import activate_anti_link_group, deactivate_anti_link_group
from takeshi_bot.errors import InvalidParameterError
from takeshi_bot.utils import is_false, is_true


async def handle(ctx: CommandContext) -> None:
    value = ctx.args[0] if ctx.args else ctx.full_args.strip()
    if is_true(value):
        activate_anti_link_group(ctx.remote_jid)
        await ctx.send_success_reply("Anti-link ativado!")
    elif is_false(value):
        deactivate_anti_link_group(ctx.remote_jid)
        await ctx.send_success_reply("Anti-link desativado!")
    else:
        raise InvalidParameterError("Use on/off.")


command = Command(
    name="anti-link",
    description="Ativa ou desativa o anti-link.",
    commands=["anti-link", "antilink"],
    usage="/anti-link on",
    handle=handle,
)
