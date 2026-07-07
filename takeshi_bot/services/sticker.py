from __future__ import annotations

from pathlib import Path

from takeshi_bot.context import CommandContext
from takeshi_bot.errors import InvalidParameterError
from takeshi_bot.paths import TEMP_DIR
from takeshi_bot.services.ffmpeg import Ffmpeg
from takeshi_bot.utils import get_nested_message, random_name, remove_file_if_exists


MAX_VIDEO_STICKER_DURATION_SECONDS = 10


def _video_duration_seconds(ctx: CommandContext) -> int | None:
    video_message = get_nested_message(ctx.web_message, "video") or {}
    seconds = video_message.get("seconds")
    return seconds if isinstance(seconds, int) else None


def _validate_video_sticker_duration(ctx: CommandContext) -> None:
    seconds = _video_duration_seconds(ctx)
    if not seconds or seconds > MAX_VIDEO_STICKER_DURATION_SECONDS:
        raise InvalidParameterError(
            "O video enviado tem mais de "
            f"{MAX_VIDEO_STICKER_DURATION_SECONDS} segundos! "
            "Envie um video menor."
        )


async def create_sticker(ctx: CommandContext) -> str:
    if not ctx.is_image and not ctx.is_video:
        raise InvalidParameterError(
            "Voce precisa marcar ou responder a uma imagem/gif/video!"
        )

    ffmpeg = Ffmpeg()
    input_path: str | None = None
    output_path = str(TEMP_DIR / random_name("webp"))
    final_path = str(TEMP_DIR / random_name("webp"))

    try:
        if ctx.is_image:
            input_path = await ctx.download_image("sticker-input")
            if not input_path:
                raise RuntimeError("Nao consegui baixar a imagem.")
            await ffmpeg.execute(
                "-i",
                input_path,
                "-vf",
                "scale=512:512:force_original_aspect_ratio=decrease,"
                "pad=512:512:(ow-iw)/2:(oh-ih)/2",
                "-f",
                "webp",
                "-quality",
                "90",
                output_path,
            )
        else:
            _validate_video_sticker_duration(ctx)
            input_path = await ctx.download_video("sticker-input")
            if not input_path:
                raise RuntimeError("Nao consegui baixar o video.")
            await ffmpeg.execute(
                "-i",
                input_path,
                "-vf",
                "scale=350:350:force_original_aspect_ratio=decrease,fps=15",
                "-c:v",
                "libwebp",
                "-loop",
                "0",
                "-quality",
                "8",
                "-compression_level",
                "6",
                "-method",
                "6",
                "-preset",
                "picture",
                "-an",
                "-f",
                "webp",
                output_path,
            )
        await ctx.bridge.add_sticker_metadata(
            output_path,
            final_path,
            {
                "packName": ctx.web_message.get("pushName")
                or ctx.web_message.get("notifyName")
                or (ctx.user_lid or "usuario").replace("@lid", ""),
                "packPublisher": f"{ctx.prefix} {ctx.command_name}".strip()
                or "Takeshi Bot",
            },
        )
        await ctx.send_sticker_from_file(final_path)
        return final_path
    finally:
        if input_path:
            await ffmpeg.cleanup(input_path)
        remove_file_if_exists(output_path)
        remove_file_if_exists(final_path)


def is_animated_sticker(file_path: str) -> bool:
    data = Path(file_path).read_bytes()
    return b"ANIM" in data or b"ANMF" in data
