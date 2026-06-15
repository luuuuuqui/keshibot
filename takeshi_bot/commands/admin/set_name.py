from __future__ import annotations

from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext
from takeshi_bot.errors import InvalidParameterError, WarningError


async def handle(ctx: CommandContext) -> None:
    if not ctx.is_group:
        raise WarningError("Esse comando so pode ser usado em grupos.")
    name = ctx.full_args.strip()
    if not name:
        raise InvalidParameterError("Voce precisa fornecer um novo nome para o grupo!")
    if len(name) < 3 or len(name) > 40:
        raise InvalidParameterError("O nome do grupo deve ter entre 3 e 40 caracteres!")
    await ctx.send_wait_reply("Alterando o nome do grupo...")
    old_name = await ctx.get_group_name() or ""
    await ctx.bridge.group_update_subject(ctx.remote_jid, name)
    await ctx.send_success_reply(
        f"Nome do grupo alterado com sucesso!\n\n*Antigo*: {old_name}\n\n*Novo*: {name}"
    )


command = Command(
    name="set-name",
    description="Altera o nome do grupo.",
    commands=["set-name", "set-group-name", "mudar-nome-grupo", "nome-grupo"],
    usage="/set-name novo nome",
    handle=handle,
)
