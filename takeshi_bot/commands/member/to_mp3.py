from __future__ import annotations

from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext
from takeshi_bot.errors import InvalidParameterError
from takeshi_bot.services.ffmpeg import Ffmpeg


async def handle(ctx: CommandContext) -> None:
    if not ctx.is_video:
        raise InvalidParameterError("Voce precisa marcar ou responder a um video!")

    ffmpeg = Ffmpeg()
    input_path = await ctx.download_video("to-mp3-input")
    output_path = None
    try:
        if not input_path:
            raise RuntimeError("Nao consegui baixar o video.")
        output_path = await ffmpeg.extract_audio_to_mp3(input_path)
        await ctx.send_audio_from_file(output_path)
    finally:
        await ffmpeg.cleanup(input_path)
        await ffmpeg.cleanup(output_path)


command = Command(
    name="to-mp3",
    description="Converte video em audio MP3.",
    commands=["to-mp3", "video2mp3", "tomp3"],
    usage="/to-mp3",
    handle=handle,
)
