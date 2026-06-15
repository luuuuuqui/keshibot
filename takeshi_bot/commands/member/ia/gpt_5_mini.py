from __future__ import annotations

from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext
from takeshi_bot.errors import InvalidParameterError
from takeshi_bot.services.spider_x_api import gpt5_mini


async def handle(ctx: CommandContext) -> None:
    text = ctx.full_args.strip()
    if not text:
        raise InvalidParameterError("Informe uma pergunta.")
    await ctx.send_wait_reply()
    response = await gpt5_mini(text)
    await ctx.send_reply(response)


command = Command(
    name="gpt-5-mini",
    description="Conversa com GPT-5 Mini via Spider X.",
    commands=["gpt-5-mini", "gpt-5", "gpt", "gpt5mini"],
    usage="/gpt-5-mini pergunta",
    handle=handle,
)
