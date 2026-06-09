from __future__ import annotations

from pathlib import Path

from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext
from takeshi_bot.errors import InvalidParameterError
from takeshi_bot.services.spider_x_api import to_gif
from takeshi_bot.utils import random_name, remove_file_if_exists


async def handle(ctx: CommandContext) -> None:
    if not ctx.is_sticker:
        raise InvalidParameterError("Voce precisa enviar uma figurinha!")
    await ctx.send_react("\u23f3")
    sticker_path = await ctx.download_sticker(random_name("sticker"))
    try:
        if not sticker_path:
            raise RuntimeError("Nao consegui baixar a figurinha.")
        gif_url = await to_gif(Path(sticker_path).read_bytes())
        await ctx.send_react("\u2705")
        await ctx.send_gif_from_url(gif_url)
    finally:
        remove_file_if_exists(sticker_path)


command = Command(
    name="togif",
    description="Transforma figurinhas animadas em GIF.",
    commands=["togif", "gif"],
    usage="/togif",
    handle=handle,
)
