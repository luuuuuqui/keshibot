from __future__ import annotations

from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext


async def handle(ctx: CommandContext) -> None:
    await ctx.bridge.group_setting_update(ctx.remote_jid, "announcement")
    await ctx.send_success_reply("Grupo fechado com sucesso!")


command = Command(
    name="fechar",
    description="Fecha o grupo.",
    commands=["fechar", "fecha", "fechar-grupo", "fecha-grupo", "close", "close-group"],
    usage="/fechar",
    handle=handle,
)
