from __future__ import annotations

from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext
from takeshi_bot.errors import InvalidParameterError
from ._helpers import send_youtube_audio


async def handle(ctx: CommandContext) -> None:
    query = ctx.full_args.strip()
    if "http://" in query or "https://" in query:
        raise InvalidParameterError("Voce nao pode usar links aqui! Use /yt-mp3 link")
    await send_youtube_audio(ctx, query, by_search=True)


command = Command(
    name="play-audio",
    description="Baixa musicas por pesquisa.",
    commands=["play-audio", "play", "pa"],
    usage="/play-audio MC Hariel",
    handle=handle,
)
