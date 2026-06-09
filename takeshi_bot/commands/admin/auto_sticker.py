from __future__ import annotations

from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext
from takeshi_bot.database import (
    activate_auto_sticker_group,
    deactivate_auto_sticker_group,
    is_active_auto_sticker_group,
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
    active = is_active_auto_sticker_group(ctx.remote_jid)
    if (turn_on and active) or (turn_off and not active):
        raise WarningError(
            f"O recurso de auto-figurinha ja esta {'ativado' if turn_on else 'desativado'}!"
        )
    if turn_on:
        activate_auto_sticker_group(ctx.remote_jid)
    else:
        deactivate_auto_sticker_group(ctx.remote_jid)
    await ctx.send_success_reply(
        f"Recurso de auto-figurinha {'ativado' if turn_on else 'desativado'} com sucesso!"
    )


command = Command(
    name="auto-sticker",
    description="Ativa/desativa auto-figurinha no grupo.",
    commands=["auto-sticker", "auto-figu", "auto-fig", "auto-stick"],
    usage="/auto-sticker 1",
    handle=handle,
)
