from __future__ import annotations

from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext
from takeshi_bot.errors import InvalidParameterError, WarningError
from takeshi_bot.services.spider_x_api import download


async def handle(ctx: CommandContext) -> None:
    url = ctx.full_args.strip()
    if not url:
        raise InvalidParameterError("Voce precisa enviar uma URL do TikTok!")
    if "tiktok.com" not in url:
        raise WarningError("O link nao e do TikTok!")
    await ctx.send_react("\u23f3")
    data = await download("tik-tok-audio", url)
    media_url = data.get("url") or data.get("audio") or data.get("audio_url")
    if not media_url:
        await ctx.send_error_reply("Nenhum resultado encontrado!")
        return
    await ctx.send_react("\u2705")
    await ctx.send_audio_from_url(media_url)


command = Command(
    name="tik-tok-audio",
    description="Baixa audio do TikTok.",
    commands=["tik-tok-audio", "tiktok-audio", "ttk-audio"],
    usage="/tik-tok-audio https://tiktok.com/...",
    handle=handle,
)
