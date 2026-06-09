from __future__ import annotations

from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext
from takeshi_bot.errors import InvalidParameterError
from takeshi_bot.services.spider_x_api import set_proxy


async def handle(ctx: CommandContext) -> None:
    if not ctx.args:
        raise InvalidParameterError("Voce precisa fornecer uma proxy valida!")
    await ctx.send_react("\u23f3")
    if not await set_proxy(ctx.args[0].strip()):
        await ctx.send_error_reply("Nao foi possivel definir a proxy! Tente novamente!")
        return
    await ctx.send_success_reply("Proxy definida com sucesso na Spider X API!")


command = Command(
    name="set-proxy",
    description="Troca a proxy da Spider X API.",
    commands=["set-proxy"],
    usage="/set-proxy <nova_proxy>",
    handle=handle,
)
