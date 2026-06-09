from __future__ import annotations

from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext
from takeshi_bot.database import check_if_member_is_muted, unmute_member
from takeshi_bot.errors import DangerError
from takeshi_bot.utils import only_numbers


async def handle(ctx: CommandContext) -> None:
    if not ctx.is_group:
        raise DangerError("Este comando so pode ser usado em grupos.")
    user_id = ctx.reply_lid or (f"{only_numbers(ctx.args[0])}@lid" if ctx.args else None)
    if not user_id:
        raise DangerError("Voce precisa mencionar um usuario ou responder a mensagem dele.")
    if not check_if_member_is_muted(ctx.remote_jid, user_id):
        await ctx.send_error_reply(f"O usuario @{only_numbers(user_id)} nao esta silenciado.")
        return
    unmute_member(ctx.remote_jid, user_id)
    await ctx.send_success_reply(f"@{only_numbers(user_id)} foi desmutado com sucesso!")


command = Command(
    name="unmute",
    description="Remove o silencio de um usuario.",
    commands=["unmute", "desmutar"],
    usage="/unmute @usuario",
    handle=handle,
)
