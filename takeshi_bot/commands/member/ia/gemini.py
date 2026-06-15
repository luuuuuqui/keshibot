from __future__ import annotations

from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext
from takeshi_bot.errors import InvalidParameterError
from takeshi_bot.services.spider_x_api import gemini


async def handle(ctx: CommandContext) -> None:
    text = ctx.full_args.strip()
    if not text:
        raise InvalidParameterError("Informe uma pergunta.")
    await ctx.send_wait_reply()
    response = await gemini(text)
    await ctx.send_reply(response)


command = Command(
    name="gemini",
    description="Conversa com Gemini via Spider X.",
    commands=["gemini", "takeshi"],
    usage="/gemini pergunta",
    handle=handle,
)
