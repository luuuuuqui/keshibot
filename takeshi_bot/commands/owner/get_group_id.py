from __future__ import annotations

from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext
from takeshi_bot.errors import WarningError


async def handle(ctx: CommandContext) -> None:
    if not ctx.is_group:
        raise WarningError("Este comando deve ser usado dentro de um grupo.")
    await ctx.send_success_reply(f"*ID do grupo*: {ctx.remote_jid}")


command = Command(
    name="get-group-id",
    description="Retorna o ID completo de um grupo.",
    commands=["get-group-id", "id-get", "id-group"],
    usage="/get-group-id",
    handle=handle,
)
