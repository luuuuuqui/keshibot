from __future__ import annotations

from takeshi_bot import config
from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext
from takeshi_bot.errors import DangerError, InvalidParameterError
from takeshi_bot.utils import only_numbers
from takeshi_bot.utils.warn_system import add_warn, get_warn_limit


async def handle(ctx: CommandContext) -> None:
    if not ctx.args and not ctx.is_reply:
        raise InvalidParameterError("Mencione um usuario ou responda a uma mensagem.")
    if ctx.args and "@" not in ctx.args[0]:
        raise InvalidParameterError('Use "@" ao mencionar um usuario.')

    target_lid = ctx.reply_lid if ctx.is_reply else f"{only_numbers(ctx.args[0])}@lid"
    if not target_lid:
        raise InvalidParameterError("Membro invalido!")
    if target_lid == ctx.user_lid:
        raise DangerError("Voce nao pode se advertir!")
    if target_lid in {config.BOT_LID, config.OWNER_LID}:
        raise DangerError("Nao e possivel advertir este usuario.")

    reason = " ".join(ctx.args[1:]) or "Advertencia generica"
    new_count = add_warn(ctx.remote_jid, target_lid, reason)
    limit = get_warn_limit(ctx.remote_jid)
    await ctx.send_reply(
        f"\u26a0\ufe0f *@{target_lid.split('@')[0]}* foi advertido!\n"
        f'Motivo: _"{reason}"_\n'
        f"Total: {new_count}/{limit} advertencias",
        [target_lid],
    )
    if new_count >= limit:
        await ctx.bridge.group_participants_update(ctx.remote_jid, [target_lid], "remove")
        await ctx.send_reply("\u274c Limite de advertencias atingido. Usuario removido.")


command = Command(
    name="warn",
    description="Aplica advertencia a um membro.",
    commands=["warn", "advertir", "adverter", "advt"],
    usage="/warn @usuario motivo",
    handle=handle,
)
