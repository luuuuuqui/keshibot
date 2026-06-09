from __future__ import annotations

from takeshi_bot import config
from takeshi_bot.commands import Command
from takeshi_bot.commands.registry import registry
from takeshi_bot.context import CommandContext
from takeshi_bot.database import get_prefix


async def handle(ctx: CommandContext) -> None:
    prefix = get_prefix(ctx.remote_jid)
    groups = registry.all_commands()
    lines = [f"*{config.BOT_NAME}*", "", f"Prefixo: {prefix}", ""]
    labels = {
        "owner": "Dono",
        "admin": "Admin",
        "member": "Membro",
    }
    for command_type in ("owner", "admin", "member"):
        commands = groups.get(command_type, [])
        if not commands:
            continue
        lines.append(f"*{labels[command_type]}*")
        for item in sorted(commands, key=lambda command: command.name):
            alias = item.commands[0] if item.commands else item.name
            lines.append(f"{prefix}{alias} - {item.description}")
        lines.append("")
    await ctx.send_reply("\n".join(lines).strip())


command = Command(
    name="menu",
    description="Mostra os comandos disponiveis.",
    commands=["menu", "help", "ajuda"],
    usage="/menu",
    handle=handle,
)
