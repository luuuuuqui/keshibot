from __future__ import annotations

from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext
from takeshi_bot.database import remove_auto_responder_item_by_key
from takeshi_bot.errors import InvalidParameterError


async def handle(ctx: CommandContext) -> None:
    if len(ctx.args) != 1:
        raise InvalidParameterError("Informe o ID do termo a ser removido.")
    try:
        item_id = int(ctx.args[0])
    except ValueError as error:
        raise InvalidParameterError("O ID deve ser um numero valido maior que 0.") from error
    if item_id <= 0:
        raise InvalidParameterError("O ID deve ser um numero valido maior que 0.")
    if not remove_auto_responder_item_by_key(item_id):
        await ctx.send_error_reply(f"Nao foi possivel remover o termo com ID {item_id}.")
        return
    await ctx.send_success_reply(
        f"O termo com o ID {item_id} foi removido do auto-responder com sucesso!"
    )


command = Command(
    name="delete-auto-responder",
    description="Remove termo do auto-responder pelo ID.",
    commands=[
        "delete-auto-responder",
        "delete-auto",
        "delete-responder",
        "del-auto",
        "del-responder",
        "remove-auto-responder",
        "remove-auto",
        "remove-responder",
    ],
    usage="/delete-auto-responder 1",
    handle=handle,
)
