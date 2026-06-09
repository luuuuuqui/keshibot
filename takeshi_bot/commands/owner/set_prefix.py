from __future__ import annotations

from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext
from takeshi_bot.database import set_prefix
from takeshi_bot.errors import InvalidParameterError


async def handle(ctx: CommandContext) -> None:
    prefix = ctx.args[0] if ctx.args else ctx.full_args.strip()
    if not prefix:
        raise InvalidParameterError("Informe o novo prefixo.")
    if len(prefix) > 3:
        raise InvalidParameterError("O prefixo deve ter no maximo 3 caracteres.")
    set_prefix(ctx.remote_jid, prefix)
    await ctx.send_success_reply(f"Prefixo alterado para: {prefix}")


command = Command(
    name="set-prefix",
    description="Define o prefixo do grupo.",
    commands=["set-prefix", "setprefix"],
    usage="/set-prefix !",
    handle=handle,
)
