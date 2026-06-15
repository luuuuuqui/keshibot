from __future__ import annotations

from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext
from takeshi_bot.errors import InvalidParameterError
from takeshi_bot.services.spider_x_api import deepseek_v4_flash


async def handle(ctx: CommandContext) -> None:
    text = ctx.full_args.strip()
    if not text:
        raise InvalidParameterError("Informe uma pergunta.")
    await ctx.send_wait_reply()
    await ctx.send_reply(await deepseek_v4_flash(text))


command = Command(
    name="deepseek",
    description="Conversa com DeepSeek via Spider X.",
    commands=["deepseek", "deep-seek"],
    usage="/deepseek pergunta",
    handle=handle,
)
