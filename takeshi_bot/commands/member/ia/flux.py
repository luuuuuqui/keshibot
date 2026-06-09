from __future__ import annotations

from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext
from takeshi_bot.errors import InvalidParameterError
from takeshi_bot.services.spider_x_api import image_ai


async def handle(ctx: CommandContext) -> None:
    prompt = ctx.full_args.strip()
    if not prompt:
        raise InvalidParameterError("Voce precisa fornecer uma descricao para a imagem.")
    await ctx.send_wait_reply("gerando imagem...")
    data = await image_ai(prompt)
    if not data.get("image"):
        await ctx.send_warning_reply("Nao foi possivel gerar a imagem.")
        return
    await ctx.send_react("\u2705")
    await ctx.send_image_from_url(data["image"])


command = Command(
    name="flux",
    description="Cria imagem usando IA Flux.",
    commands=["flux"],
    usage="/flux descricao",
    handle=handle,
)
