from __future__ import annotations

from datetime import datetime

from takeshi_bot import config
from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext
from takeshi_bot.errors import DangerError, InvalidParameterError
from takeshi_bot.utils import only_numbers
from takeshi_bot.utils.warn_system import get_all_warns, reactivate_warn_by_index


async def handle(ctx: CommandContext) -> None:
    if ctx.is_reply and ctx.reply_lid:
        target_lid = ctx.reply_lid
    elif ctx.args and "@" in ctx.args[0]:
        target_lid = f"{only_numbers(ctx.args[0])}@lid"
    else:
        raise InvalidParameterError("Mencione um usuario ou responda a uma mensagem.")
    if target_lid in {config.BOT_LID, config.OWNER_LID}:
        raise DangerError("Nao e possivel alterar advertencias deste usuario.")

    action = ctx.args[1].lower() if len(ctx.args) > 1 else ""
    invalid_warns = [warn for warn in get_all_warns(ctx.remote_jid, target_lid) if not warn.get("valid")]
    if not invalid_warns:
        await ctx.send_reply("Usuario nao tem advertencias invalidas.")
        return
    if action == "list":
        lines = [f"*Advertencias invalidas de @{target_lid.split('@')[0]}:*", ""]
        for index, warn in enumerate(invalid_warns, start=1):
            date = datetime.fromtimestamp(warn.get("timestamp", 0) / 1000).strftime("%d/%m/%Y")
            lines.append(f"{index}. \"{warn.get('reason')}\" ({date})")
        await ctx.send_reply("\n".join(lines), [target_lid])
        return
    index = int(action) - 1 if action.isdigit() else len(invalid_warns) - 1
    if reactivate_warn_by_index(ctx.remote_jid, target_lid, index):
        await ctx.send_reply(f"\u2705 Advertencia #{index + 1} reativada.")
    else:
        await ctx.send_reply("\u274c Falha ao reativar advertencia.")


command = Command(
    name="warn-reactivate",
    description="Reativa uma advertencia invalida.",
    commands=["warn-reactivate", "reativarwarn", "reativaradvertencia", "reativaradvt"],
    usage="/warn-reactivate @usuario [list|numero]",
    handle=handle,
)
