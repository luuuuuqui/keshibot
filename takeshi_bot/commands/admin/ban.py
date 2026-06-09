from __future__ import annotations

from takeshi_bot import config
from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext
from takeshi_bot.errors import DangerError, InvalidParameterError
from takeshi_bot.utils import only_numbers


def _target_lid(ctx: CommandContext) -> str | None:
    if ctx.is_reply:
        return ctx.reply_lid
    if ctx.args and "@" in ctx.args[0]:
        return f"{only_numbers(ctx.args[0])}@lid"
    return None


async def handle(ctx: CommandContext) -> None:
    if not ctx.args and not ctx.is_reply:
        raise InvalidParameterError("Voce precisa mencionar ou marcar um membro!")
    if ctx.args and not ctx.is_reply and "@" not in ctx.args[0]:
        raise InvalidParameterError('Voce precisa mencionar um membro com "@"!')
    target = _target_lid(ctx)
    if not target:
        raise InvalidParameterError("Membro invalido!")
    if target == ctx.user_lid:
        raise DangerError("Voce nao pode remover voce mesmo!")
    if target == config.OWNER_LID:
        raise DangerError("Voce nao pode remover o dono do bot!")
    if target == config.BOT_LID:
        raise DangerError("Voce nao pode me remover!")
    await ctx.bridge.group_participants_update(ctx.remote_jid, [target], "remove")
    await ctx.send_success_reply("Membro removido com sucesso!")


command = Command(
    name="ban",
    description="Remove um membro do grupo.",
    commands=["ban", "kick"],
    usage="/ban @membro",
    handle=handle,
)
