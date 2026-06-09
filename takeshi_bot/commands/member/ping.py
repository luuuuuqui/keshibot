from __future__ import annotations

import time

from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext


async def handle(ctx: CommandContext) -> None:
    elapsed = 0.0
    if ctx.start_process:
        elapsed = max(0.0, time.time() - ctx.start_process)
    await ctx.send_success_reply(f"Pong! Tempo de resposta: {elapsed:.2f}s")


command = Command(
    name="ping",
    description="Verifica se o bot esta respondendo.",
    commands=["ping"],
    usage="/ping",
    handle=handle,
)
