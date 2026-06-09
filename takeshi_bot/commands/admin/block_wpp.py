from __future__ import annotations

from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext
from takeshi_bot.errors import InvalidParameterError
from takeshi_bot.utils import to_user_jid


async def handle(ctx: CommandContext) -> None:
    if len(ctx.args) != 1:
        raise InvalidParameterError("Informe um telefone valido. Exemplo: /block-wpp +5541123456789")
    await ctx.bridge.update_block_status(to_user_jid(ctx.args[0]), "block")
    await ctx.send_success_reply("Numero bloqueado com sucesso!")


command = Command(
    name="block-wpp",
    description="Bloqueia um numero no WhatsApp do bot.",
    commands=["block-wpp", "blok-wpp", "bloquear-wpp"],
    usage="/block-wpp <telefone>",
    handle=handle,
)
