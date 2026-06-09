from __future__ import annotations

from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext
from takeshi_bot.database import set_spider_api_token
from takeshi_bot.errors import InvalidParameterError


async def handle(ctx: CommandContext) -> None:
    token = ctx.full_args.strip()
    if not token:
        raise InvalidParameterError("Informe o token da Spider X API.")
    set_spider_api_token(token)
    await ctx.send_success_reply("Token da Spider X API configurado!")


command = Command(
    name="set-spider-api-token",
    description="Configura o token da Spider X API.",
    commands=["set-spider-api-token", "setspiderapitoken"],
    usage="/set-spider-api-token seu_token",
    handle=handle,
)
