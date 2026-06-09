from __future__ import annotations

from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext


async def handle(ctx: CommandContext) -> None:
    await ctx.send_reply(f"Seu LID: {ctx.user_lid or 'indisponivel'}")


command = Command(
    name="meu-lid",
    description="Mostra o seu LID.",
    commands=["meu-lid", "meulid"],
    usage="/meu-lid",
    handle=handle,
)
