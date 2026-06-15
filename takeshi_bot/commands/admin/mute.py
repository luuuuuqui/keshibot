from __future__ import annotations

from takeshi_bot import config
from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext
from takeshi_bot.database import check_if_member_is_muted, mute_member
from takeshi_bot.errors import DangerError
from takeshi_bot.utils import as_dict, as_list, only_numbers


async def handle(ctx: CommandContext) -> None:
    if not ctx.is_group:
        raise DangerError("Este comando so pode ser usado em grupos.")
    if not ctx.args and not ctx.reply_lid:
        raise DangerError("Voce precisa mencionar um usuario ou responder a mensagem dele.")
    user_id = ctx.reply_lid or (f"{only_numbers(ctx.args[0])}@lid" if ctx.args else None)
    if not user_id:
        raise DangerError("Usuario invalido.")
    if user_id == config.OWNER_LID:
        raise DangerError("Voce nao pode mutar o dono do bot!")
    if user_id == config.BOT_LID:
        raise DangerError("Voce nao pode mutar o bot.")
    metadata = await ctx.bridge.group_metadata(ctx.remote_jid)
    participants = [as_dict(item) for item in as_list(metadata.get("participants"))]
    if not any(item.get("id") == user_id for item in participants):
        await ctx.send_error_reply(f"O usuario @{only_numbers(user_id)} nao esta neste grupo.")
        return
    if any(item.get("id") == user_id and item.get("admin") for item in participants):
        raise DangerError("Voce nao pode mutar um administrador.")
    if check_if_member_is_muted(ctx.remote_jid, user_id):
        await ctx.send_error_reply(f"O usuario @{only_numbers(user_id)} ja esta silenciado.")
        return
    mute_member(ctx.remote_jid, user_id)
    await ctx.send_success_reply(f"@{only_numbers(user_id)} foi mutado com sucesso!")


command = Command(
    name="mute",
    description="Silencia um usuario no grupo.",
    commands=["mute", "mutar"],
    usage="/mute @usuario",
    handle=handle,
)
