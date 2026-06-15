from __future__ import annotations

from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext
from takeshi_bot.errors import InvalidParameterError, WarningError
from takeshi_bot.services.spider_x_api import search
from takeshi_bot.utils import as_dict, as_list


async def handle(ctx: CommandContext) -> None:
    query = ctx.full_args.strip()
    if len(query) <= 1:
        raise InvalidParameterError("Voce precisa fornecer uma pesquisa para o YouTube.")
    if len(query) > 100:
        raise InvalidParameterError("O tamanho maximo da pesquisa e de 100 caracteres.")
    data = await search("youtube", query)
    if not data:
        raise WarningError("Nao foi possivel encontrar resultados para a pesquisa.")
    lines: list[str] = []
    for item in as_list(data)[:8]:
        result = as_dict(item)
        lines.append(
            f"Titulo: *{result.get('title', '')}*\n"
            f"Duracao: {result.get('duration', '')}\n"
            f"Publicado em: {result.get('published_at', '')}\n"
            f"Views: {result.get('views', '')}\n"
            f"URL: {result.get('url', '')}"
        )
    await ctx.send_success_reply(
        f"*Pesquisa realizada*\n\n*Termo*: {query}\n\n*Resultados*\n" + "\n\n-----\n\n".join(lines)
    )


command = Command(
    name="yt-search",
    description="Pesquisa videos no YouTube.",
    commands=["yt-search", "youtube-search"],
    usage="/yt-search MC Hariel",
    handle=handle,
)
