from __future__ import annotations

from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext
from takeshi_bot.database import deactivate_group


async def handle(ctx: CommandContext) -> None:
    deactivate_group(ctx.remote_jid)
    await ctx.send_success_reply("Bot desativado neste grupo!")


command = Command(
    name="off",
    description="Desativa o bot no grupo atual.",
    commands=["off", "desligar"],
    usage="/off",
    handle=handle,
)
