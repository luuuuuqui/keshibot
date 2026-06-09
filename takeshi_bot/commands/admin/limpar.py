from __future__ import annotations

from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext
from takeshi_bot.errors import WarningError
from takeshi_bot.messages import clear_chat


async def handle(ctx: CommandContext) -> None:
    if not ctx.is_group:
        raise WarningError("Esse comando so pode ser usado em grupos.")
    await ctx.send_text(clear_chat())
    await ctx.send_success_reply("Chat limpo com sucesso!")


command = Command(
    name="limpar-chat",
    description="Limpa visualmente o historico do grupo.",
    commands=[
        "limpar-chat",
        "clean-chat",
        "clean",
        "clear-chat",
        "clear",
        "lc",
        "limpa-chat",
        "limpa",
        "limpar",
    ],
    usage="/limpar-chat",
    handle=handle,
)
