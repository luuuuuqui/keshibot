from __future__ import annotations

from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext
from takeshi_bot.errors import InvalidParameterError
from takeshi_bot.services.ffmpeg import Ffmpeg


async def handle(ctx: CommandContext) -> None:
    if not ctx.is_sticker:
        raise InvalidParameterError("Voce precisa marcar ou responder a um sticker!")

    ffmpeg = Ffmpeg()
    input_path = await ctx.download_sticker("to-image-input")
    output_path = None
    try:
        if not input_path:
            raise RuntimeError("Nao consegui baixar o sticker.")
        output_path = await ffmpeg.convert_sticker_to_image(input_path)
        await ctx.send_image_from_file(output_path)
    finally:
        await ffmpeg.cleanup(input_path)
        await ffmpeg.cleanup(output_path)


command = Command(
    name="toimage",
    description="Converte sticker em imagem.",
    commands=["toimage", "toimg"],
    usage="/toimage",
    handle=handle,
)
