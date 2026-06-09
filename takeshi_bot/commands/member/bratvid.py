from __future__ import annotations

from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext
from takeshi_bot.errors import InvalidParameterError
from takeshi_bot.services.spider_x_api import sticker_url


async def handle(ctx: CommandContext) -> None:
    text = ctx.full_args.strip()
    if not text:
        raise InvalidParameterError(
            "Voce precisa informar o texto que deseja transformar em figurinha animada."
        )
    await ctx.send_react("\u23f3")
    await ctx.send_sticker_from_url(sticker_url("abrat", text))
    await ctx.send_react("\u2705")


command = Command(
    name="bratvid",
    description="Gera figurinha animada estilo brat.",
    commands=["bratvid", "abrat"],
    usage="/bratvid texto",
    handle=handle,
)
