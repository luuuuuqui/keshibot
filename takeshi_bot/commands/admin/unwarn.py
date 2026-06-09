from __future__ import annotations

from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext
from takeshi_bot.errors import InvalidParameterError
from takeshi_bot.utils import only_numbers
from takeshi_bot.utils.warn_system import remove_last_warn


async def handle(ctx: CommandContext) -> None:
    if not ctx.args and not ctx.is_reply:
        raise InvalidParameterError("Mencione um usuario ou responda a uma mensagem.")
    target_lid = ctx.reply_lid if ctx.is_reply else f"{only_numbers(ctx.args[0])}@lid"
    if not target_lid:
        raise InvalidParameterError("Membro invalido!")
    remaining = remove_last_warn(ctx.remote_jid, target_lid)
    await ctx.send_success_reply(f"Ultima advertencia removida. Restam {remaining}.")


command = Command(
    name="unwarn",
    description="Remove a ultima advertencia valida de um membro.",
    commands=["unwarn", "remover-warn", "tirar-warn"],
    usage="/unwarn @usuario",
    handle=handle,
)
