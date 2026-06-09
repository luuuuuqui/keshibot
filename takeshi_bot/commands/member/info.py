from __future__ import annotations

from takeshi_bot.commands import Command
from takeshi_bot.commands.registry import registry
from takeshi_bot.context import CommandContext
from takeshi_bot.errors import InvalidParameterError, WarningError
from takeshi_bot.utils import format_command


async def handle(ctx: CommandContext) -> None:
    if not ctx.args:
        raise InvalidParameterError("Por favor, informe o nome do comando.")
    target = format_command(ctx.args[0])
    await ctx.send_react("\u23f3")
    for commands in registry.all_commands().values():
        for item in commands:
            aliases = [format_command(alias) for alias in item.commands]
            if target == format_command(item.name) or target in aliases:
                await ctx.send_react("\u2705")
                await ctx.send_reply(
                    "*Informacoes do comando*\n\n"
                    f"- *Nome:* _{item.name}_\n"
                    f"- *Descricao:* _{item.description}_\n"
                    f"- *Comandos:* _{', '.join(item.commands)}_\n"
                    f"- *Uso:* _{item.usage}_"
                )
                return
    raise WarningError(f'Comando "{ctx.args[0]}" nao encontrado.')


command = Command(
    name="info",
    description="Exibe informacoes de um comando.",
    commands=["info", "info-cmd", "info-comando", "info-command"],
    usage="/info <comando>",
    handle=handle,
)
