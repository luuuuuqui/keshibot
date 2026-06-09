from __future__ import annotations

from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext
from takeshi_bot.errors import InvalidParameterError, WarningError
from takeshi_bot.services.spider_x_api import download


async def handle(ctx: CommandContext) -> None:
    url = ctx.full_args.strip()
    if not url:
        raise InvalidParameterError("Voce precisa enviar uma URL do YouTube!")
    if "you" not in url:
        raise WarningError("O link nao e do YouTube!")
    await ctx.send_react("\u23f3")
    data = await download("yt-mp4", url)
    media_url = data.get("url") or data.get("video_url") or data.get("video")
    if not media_url:
        await ctx.send_error_reply("Nenhum resultado encontrado!")
        return
    await ctx.send_react("\u2705")
    await ctx.send_video_from_url(media_url)


command = Command(
    name="yt-mp4",
    description="Baixa video do YouTube por link.",
    commands=["yt-mp4", "youtube-mp4", "yt-video", "youtube-video", "mp4"],
    usage="/yt-mp4 https://youtube.com/watch?v=...",
    handle=handle,
)
