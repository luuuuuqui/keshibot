from __future__ import annotations

from pathlib import Path

from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext
from takeshi_bot.errors import DangerError, InvalidParameterError
from takeshi_bot.services.ffmpeg import Ffmpeg
from takeshi_bot.services.linker import upload
from takeshi_bot.services.spider_x_api import canvas_url
from takeshi_bot.utils import random_name, remove_file_if_exists


def make_ffmpeg_image_command(name: str, aliases: list[str], description: str, method: str) -> Command:
    async def handle(ctx: CommandContext) -> None:
        if not ctx.is_image:
            raise InvalidParameterError("Voce precisa marcar ou responder a uma imagem.")
        await ctx.send_react("\u23f3")
        ffmpeg = Ffmpeg()
        input_path = await ctx.download_image(random_name(name))
        output_path = None
        try:
            if not input_path:
                raise RuntimeError("Nao consegui baixar a imagem.")
            output_path = await getattr(ffmpeg, method)(input_path)
            await ctx.send_react("\u2705")
            await ctx.send_image_from_file(output_path)
        finally:
            remove_file_if_exists(input_path)
            remove_file_if_exists(output_path)

    return Command(name=name, description=description, commands=aliases, usage=f"/{name}", handle=handle)


def make_spider_canvas_command(name: str, aliases: list[str], description: str, canvas_type: str) -> Command:
    async def handle(ctx: CommandContext) -> None:
        if not ctx.is_image:
            raise InvalidParameterError("Voce precisa marcar ou responder a uma imagem.")
        await ctx.send_react("\u23f3")
        input_path = await ctx.download_image(random_name(name))
        try:
            if not input_path:
                raise RuntimeError("Nao consegui baixar a imagem.")
            link = await upload(Path(input_path).read_bytes(), Path(input_path).name)
            if not link:
                raise DangerError("Nao consegui fazer o upload da imagem.")
            await ctx.send_react("\u2705")
            await ctx.send_image_from_url(canvas_url(canvas_type, link), "Imagem gerada!")
        finally:
            remove_file_if_exists(input_path)

    return Command(name=name, description=description, commands=aliases, usage=f"/{name}", handle=handle)
