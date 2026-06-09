from __future__ import annotations

from pathlib import Path

from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext
from takeshi_bot.errors import InvalidParameterError
from takeshi_bot.services.ffmpeg import Ffmpeg
from takeshi_bot.services.spider_x_api import remove_bg
from takeshi_bot.utils import random_name, remove_file_if_exists


async def handle(ctx: CommandContext) -> None:
    if not ctx.is_image and not ctx.is_sticker:
        raise InvalidParameterError("Voce precisa marcar ou responder uma imagem ou figurinha!")
    await ctx.send_react("\u23f3")
    ffmpeg = Ffmpeg()
    input_path = None
    converted_path = None
    try:
        if ctx.is_image:
            input_path = await ctx.download_image(random_name("removebg"))
            if not input_path:
                raise RuntimeError("Nao consegui baixar a imagem.")
            output = await remove_bg(Path(input_path).read_bytes(), "image/png", "image.png")
            await ctx.send_react("\u2705")
            await ctx.send_image_from_buffer(output)
            return

        input_path = await ctx.download_sticker(random_name("removebg"))
        if not input_path:
            raise RuntimeError("Nao consegui baixar a figurinha.")
        converted_path = await ffmpeg.convert_sticker_to_image(input_path)
        output = await remove_bg(Path(converted_path).read_bytes(), "image/png", "sticker.png")
        await ctx.send_react("\u2705")
        await ctx.send_image_from_buffer(output)
    finally:
        remove_file_if_exists(input_path)
        remove_file_if_exists(converted_path)


command = Command(
    name="removebg",
    description="Remove fundo de imagens e figurinhas.",
    commands=["removebg", "rmbg", "remove-bg"],
    usage="/removebg",
    handle=handle,
)
