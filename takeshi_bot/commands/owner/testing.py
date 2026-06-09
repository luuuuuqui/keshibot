from __future__ import annotations

from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext


async def handle(ctx: CommandContext) -> None:
    await ctx.send_success_reply("Python port online para testes.")


command = Command(
    name="testing",
    description="Comando de testes.",
    commands=["testing", "teste"],
    usage="/testing",
    handle=handle,
)
