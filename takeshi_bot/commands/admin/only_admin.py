from __future__ import annotations

from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext
from takeshi_bot.database import activate_only_admins, deactivate_only_admins, is_active_only_admins
from takeshi_bot.errors import InvalidParameterError, WarningError
from takeshi_bot.utils import is_false, is_true


async def handle(ctx: CommandContext) -> None:
    if not ctx.args:
        raise InvalidParameterError("Voce precisa digitar 1 ou 0 (ligar ou desligar)!")
    turn_on = is_true(ctx.args[0])
    turn_off = is_false(ctx.args[0])
    if not turn_on and not turn_off:
        raise InvalidParameterError("Voce precisa digitar 1 ou 0 (ligar ou desligar)!")
    active = is_active_only_admins(ctx.remote_jid)
    if (turn_on and active) or (turn_off and not active):
        raise WarningError(
            "O recurso de somente admins usarem meus comandos ja esta "
            f"{'ativado' if turn_on else 'desativado'}!"
        )
    if turn_on:
        activate_only_admins(ctx.remote_jid)
    else:
        deactivate_only_admins(ctx.remote_jid)
    await ctx.send_success_reply(
        "Recurso de somente admins usarem meus comandos "
        f"{'ativado' if turn_on else 'desativado'} com sucesso!"
    )


command = Command(
    name="only-admin",
    description="Permite que so administradores usem comandos.",
    commands=[
        "only-admin",
        "only-adm",
        "only-administrator",
        "only-administrators",
        "only-admins",
        "so-adm",
        "so-admin",
        "so-administrador",
        "so-administradores",
        "so-admins",
    ],
    usage="/only-admin 1",
    handle=handle,
)
