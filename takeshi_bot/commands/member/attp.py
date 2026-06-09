from __future__ import annotations

from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext
from takeshi_bot.errors import InvalidParameterError
from takeshi_bot.services.spider_x_api import sticker_url


async def handle(ctx: CommandContext) -> None:
    text = ctx.full_args.strip()
    if not text:
        raise InvalidParameterError("Informe o texto do sticker.")
    await ctx.send_sticker_from_url(sticker_url("attp", text))


command = Command(
    name="attp",
    description="Cria sticker animado com texto.",
    commands=["attp"],
    usage="/attp texto",
    handle=handle,
)
