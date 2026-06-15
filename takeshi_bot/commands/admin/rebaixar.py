from __future__ import annotations

from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext
from takeshi_bot.errors import InvalidParameterError, WarningError
from takeshi_bot.utils import only_numbers


async def handle(ctx: CommandContext) -> None:
    if not ctx.is_group:
        raise WarningError("Este comando so pode ser usado em grupo!")
    if not ctx.args:
        raise InvalidParameterError("Por favor, marque um usuario para rebaixar.")
    user_lid = f"{only_numbers(ctx.args[0])}@lid"
    await ctx.bridge.group_participants_update(ctx.remote_jid, [user_lid], "demote")
    await ctx.send_success_reply("Usuario rebaixado com sucesso!")


command = Command(
    name="rebaixar",
    description="Rebaixa um administrador para membro.",
    commands=["rebaixar", "rebaixa", "demote", "remover-adm"],
    usage="/rebaixar @usuario",
    handle=handle,
)
