from __future__ import annotations

from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext
from takeshi_bot.errors import InvalidParameterError
from takeshi_bot.services.spider_x_api import play


async def handle(ctx: CommandContext) -> None:
    query = ctx.full_args.strip()
    if not query:
        raise InvalidParameterError("Voce precisa me dizer o que deseja buscar!")
    if "http://" in query or "https://" in query:
        raise InvalidParameterError("Voce nao pode usar links aqui! Use /yt-mp4 link")
    await ctx.send_react("\u23f3")
    data = await play("video", query)
    if not data:
        await ctx.send_error_reply("Nenhum resultado encontrado!")
        return
    await ctx.send_react("\u2705")
    if data.get("thumbnail"):
        await ctx.send_image_from_url(data["thumbnail"], f"*Titulo*: {data.get('title', '')}")
    await ctx.send_video_from_url(data.get("url"))


command = Command(
    name="play-video",
    description="Baixa videos por pesquisa.",
    commands=["play-video", "pv"],
    usage="/play-video MC Hariel",
    handle=handle,
)
