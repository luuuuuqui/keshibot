from __future__ import annotations

from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext
from takeshi_bot.errors import InvalidParameterError
from takeshi_bot.services.ffmpeg import Ffmpeg
from takeshi_bot.utils import random_name, remove_file_if_exists


async def handle(ctx: CommandContext) -> None:
    if not ctx.is_image and not ctx.is_video:
        raise InvalidParameterError("Voce precisa marcar uma imagem/video para revelar.")
    await ctx.send_react("\u23f3")
    ffmpeg = Ffmpeg()
    input_path = None
    output_path = None
    try:
        if ctx.is_image:
            input_path = await ctx.download_image(random_name("reveal"))
            if not input_path:
                raise RuntimeError("Nao consegui baixar a imagem.")
            output_path = await ffmpeg.normalize_image(input_path, "jpg")
            await ctx.send_image_from_file(output_path, "Aqui esta sua imagem revelada!")
        else:
            input_path = await ctx.download_video(random_name("reveal"))
            if not input_path:
                raise RuntimeError("Nao consegui baixar o video.")
            output_path = await ffmpeg.copy_video(input_path)
            await ctx.send_video_from_file(output_path, "Aqui esta seu video revelado!")
        await ctx.send_react("\u2705")
    finally:
        remove_file_if_exists(input_path)
        remove_file_if_exists(output_path)


command = Command(
    name="revelar",
    description="Revela imagem ou video de visualizacao unica.",
    commands=["revelar", "rv", "reveal"],
    usage="/revelar",
    handle=handle,
)
