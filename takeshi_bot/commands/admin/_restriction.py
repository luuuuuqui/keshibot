from __future__ import annotations

from collections.abc import Sequence

from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext
from takeshi_bot.database import is_active_group_restriction, update_is_active_group_restriction
from takeshi_bot.errors import InvalidParameterError, WarningError
from takeshi_bot.utils import is_false, is_true


def make_restriction_command(
    name: str,
    aliases: Sequence[str],
    restriction: str,
    description: str,
) -> Command:
    async def handle(ctx: CommandContext) -> None:
        if not ctx.is_group:
            raise WarningError("Este comando so deve ser usado em grupos!")
        if not ctx.args:
            raise InvalidParameterError("Voce precisa digitar 1 ou 0 (ligar ou desligar)!")

        turn_on = is_true(ctx.args[0])
        turn_off = is_false(ctx.args[0])
        if not turn_on and not turn_off:
            raise InvalidParameterError("Voce precisa digitar 1 ou 0 (ligar ou desligar)!")

        currently_active = is_active_group_restriction(ctx.remote_jid, restriction)
        if (turn_on and currently_active) or (turn_off and not currently_active):
            status = "ativado" if turn_on else "desativado"
            raise WarningError(f"O recurso de {name} ja esta {status}!")

        update_is_active_group_restriction(ctx.remote_jid, restriction, turn_on)
        status = "ativado" if turn_on else "desativado"
        await ctx.send_success_reply(f"{name} {status} com sucesso!")

    return Command(
        name=name,
        description=description,
        commands=list(aliases),
        usage=f"/{name} 1",
        handle=handle,
    )
