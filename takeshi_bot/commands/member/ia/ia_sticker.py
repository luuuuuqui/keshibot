from __future__ import annotations

from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext
from takeshi_bot.errors import InvalidParameterError
from takeshi_bot.services.spider_x_api import image_ai


async def handle(ctx: CommandContext) -> None:
    prompt = ctx.full_args.strip()
    if not prompt:
        raise InvalidParameterError("Voce precisa fornecer uma descricao.")
    await ctx.send_wait_reply("gerando sticker...")
    data = await image_ai(prompt)
    if not data.get("image"):
        await ctx.send_warning_reply("Nao foi possivel gerar a imagem.")
        return
    await ctx.send_sticker_from_url(data["image"])


command = Command(
    name="ia-sticker",
    description="Cria sticker usando IA.",
    commands=["ia-sticker", "sticker-ia"],
    usage="/ia-sticker descricao",
    handle=handle,
)
