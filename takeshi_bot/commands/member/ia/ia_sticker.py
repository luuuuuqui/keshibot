from __future__ import annotations

from pathlib import Path

from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext
from takeshi_bot.errors import InvalidParameterError
from takeshi_bot.paths import TEMP_DIR
from takeshi_bot.services.ffmpeg import Ffmpeg
from takeshi_bot.services.spider_x_api import image_ai
from takeshi_bot.utils import random_name, remove_file_if_exists


async def _download_image(url: str) -> bytes:
    import httpx

    async with httpx.AsyncClient(timeout=90) as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.content


async def handle(ctx: CommandContext) -> None:
    prompt = ctx.full_args.strip()
    if not prompt:
        raise InvalidParameterError("Voce precisa fornecer uma descricao.")
    await ctx.send_wait_reply("gerando sticker...")
    data = await image_ai(prompt)
    image_url = data.get("image")
    if not image_url:
        await ctx.send_warning_reply("Nao foi possivel gerar a imagem.")
        return

    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    input_path = str(TEMP_DIR / random_name("png"))
    output_path = str(TEMP_DIR / random_name("webp"))
    try:
        Path(input_path).write_bytes(await _download_image(image_url))

        await Ffmpeg().execute(
            "-i",
            input_path,
            "-vf",
            "scale=512:512:force_original_aspect_ratio=decrease",
            "-f",
            "webp",
            "-quality",
            "90",
            output_path,
        )
        await ctx.send_react("\u2705")
        await ctx.send_sticker_from_file(output_path)
    finally:
        remove_file_if_exists(input_path)
        remove_file_if_exists(output_path)


command = Command(
    name="ia-sticker",
    description="Cria sticker usando IA.",
    commands=["ia-sticker", "ia-fig", "sticker-ia"],
    usage="/ia-sticker descricao",
    handle=handle,
)
