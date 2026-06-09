from __future__ import annotations

from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext
from takeshi_bot.database import activate_group


async def handle(ctx: CommandContext) -> None:
    activate_group(ctx.remote_jid)
    await ctx.send_success_reply("Bot ativado neste grupo!")


command = Command(
    name="on",
    description="Ativa o bot no grupo atual.",
    commands=["on", "ligar"],
    usage="/on",
    handle=handle,
)
