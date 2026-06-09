from __future__ import annotations

from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext
from takeshi_bot.errors import WarningError
from ._helpers import send_youtube_audio


async def handle(ctx: CommandContext) -> None:
    url = ctx.full_args.strip()
    if "you" not in url:
        raise WarningError("O link nao e do YouTube!")
    await send_youtube_audio(ctx, url, by_search=False)


command = Command(
    name="yt-mp3",
    description="Baixa audio do YouTube por link.",
    commands=["yt-mp3", "youtube-mp3", "yt-audio", "youtube-audio", "mp3"],
    usage="/yt-mp3 https://youtube.com/watch?v=...",
    handle=handle,
)
