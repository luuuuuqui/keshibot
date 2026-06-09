from __future__ import annotations

from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext
from takeshi_bot.errors import InvalidParameterError
from takeshi_bot.services.spider_x_api import pinterest


async def handle(ctx: CommandContext) -> None:
    query = ctx.full_args.strip()
    if not query:
        raise InvalidParameterError("Voce precisa me dizer o que deseja buscar no Pinterest!")
    await ctx.send_react("\u23f3")
    data = await pinterest(query)
    if not isinstance(data, list) or not data:
        await ctx.send_error_reply("Nenhuma imagem foi encontrada para a sua busca.")
        return
    first = next((item for item in data if isinstance(item, dict) and item.get("url")), None)
    if not first:
        await ctx.send_error_reply("Nao foi possivel montar resultado com as imagens retornadas.")
        return
    await ctx.send_react("\u2705")
    await ctx.send_image_from_url(first["url"], f"Resultado do Pinterest para: {query}")


command = Command(
    name="pinterest",
    description="Busca imagens no Pinterest.",
    commands=["pinterest", "pin"],
    usage="/pinterest gatos fofos",
    handle=handle,
)
