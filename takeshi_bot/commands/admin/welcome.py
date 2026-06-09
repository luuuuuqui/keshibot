from __future__ import annotations

from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext
from takeshi_bot.database import (
    activate_welcome_group,
    deactivate_welcome_group,
    is_active_welcome_group,
)
from takeshi_bot.errors import InvalidParameterError, WarningError
from takeshi_bot.utils import is_false, is_true


async def handle(ctx: CommandContext) -> None:
    if not ctx.args:
        raise InvalidParameterError("Voce precisa digitar 1 ou 0 (ligar ou desligar)!")
    turn_on = is_true(ctx.args[0])
    turn_off = is_false(ctx.args[0])
    if not turn_on and not turn_off:
        raise InvalidParameterError("Voce precisa digitar 1 ou 0 (ligar ou desligar)!")
    active = is_active_welcome_group(ctx.remote_jid)
    if (turn_on and active) or (turn_off and not active):
        raise WarningError(
            f"O recurso de boas-vindas ja esta {'ativado' if turn_on else 'desativado'}!"
        )
    if turn_on:
        activate_welcome_group(ctx.remote_jid)
    else:
        deactivate_welcome_group(ctx.remote_jid)
    await ctx.send_success_reply(
        f"Recurso de boas-vindas {'ativado' if turn_on else 'desativado'} com sucesso!"
    )


command = Command(
    name="welcome",
    description="Ativa/desativa boas-vindas no grupo.",
    commands=[
        "welcome",
        "bemvindo",
        "boasvinda",
        "boasvindas",
        "boavinda",
        "boavindas",
        "welkom",
        "welkon",
    ],
    usage="/welcome 1",
    handle=handle,
)
