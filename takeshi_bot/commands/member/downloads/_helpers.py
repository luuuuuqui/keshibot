from __future__ import annotations

from typing import Any

from takeshi_bot.context import CommandContext
from takeshi_bot.errors import InvalidParameterError, WarningError
from takeshi_bot.services.spider_x_api import download, play


def _first_url(data: dict[str, Any], *keys: str) -> str | None:
    for key in keys:
        value = data.get(key)
        if isinstance(value, str) and value:
            return value
    for key in ("url", "download_url", "audio", "video"):
        value = data.get(key)
        if isinstance(value, str) and value:
            return value
    return None


async def send_download_video(
    ctx: CommandContext, service_type: str, required_domain: str | None = None
) -> None:
    url = ctx.full_args.strip()
    if not url:
        raise InvalidParameterError("Voce precisa enviar uma URL!")
    if required_domain and required_domain not in url:
        raise WarningError(f"O link nao e de {required_domain}!")
    await ctx.send_react("\u23f3")
    data = await download(service_type, url)
    media_url = _first_url(data, "url", "video_url", "video")
    if not media_url:
        await ctx.send_error_reply("Nenhum resultado encontrado!")
        return
    await ctx.send_react("\u2705")
    await ctx.send_video_from_url(media_url)


async def send_youtube_audio(ctx: CommandContext, query_or_url: str, by_search: bool) -> None:
    if not query_or_url:
        raise InvalidParameterError("Voce precisa informar o que deseja buscar!")
    await ctx.send_react("\u23f3")
    data = await (play("audio", query_or_url) if by_search else download("yt-mp3", query_or_url))
    media_url = _first_url(data, "url", "audio_url", "audio")
    if not media_url:
        await ctx.send_error_reply("Nenhum resultado encontrado!")
        return
    await ctx.send_react("\u2705")
    thumbnail = data.get("thumbnail")
    title = data.get("title") or "Resultado"
    description = data.get("description") or ""
    channel = (data.get("channel") or {}).get("name") or ""
    if thumbnail:
        await ctx.send_image_from_url(
            thumbnail,
            f"*Titulo*: {title}\n\n*Descricao*: {description}\n*Canal*: {channel}",
        )
    await ctx.send_audio_from_url(media_url)
