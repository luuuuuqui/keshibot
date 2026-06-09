from __future__ import annotations

from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext


async def handle(ctx: CommandContext) -> None:
    await ctx.bridge.group_setting_update(ctx.remote_jid, "not_announcement")
    await ctx.send_success_reply("Grupo aberto com sucesso!")


command = Command(
    name="abrir",
    description="Abre o grupo.",
    commands=[
        "abrir",
        "abri",
        "abre",
        "abrir-grupo",
        "abri-grupo",
        "abre-grupo",
        "open",
        "open-group",
    ],
    usage="/abrir",
    handle=handle,
)
