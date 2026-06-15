from __future__ import annotations

from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext
from takeshi_bot.database import add_auto_responder_item
from takeshi_bot.errors import InvalidParameterError


async def handle(ctx: CommandContext) -> None:
    if len(ctx.args) < 2:
        raise InvalidParameterError("Use: /add-auto-responder gatilho / resposta")
    add_auto_responder_item(ctx.args[0], ctx.args[1])
    await ctx.send_success_reply("Resposta automatica cadastrada!")


command = Command(
    name="add-auto-responder",
    description="Adiciona uma resposta automatica.",
    commands=["add-auto-responder", "add-auto", "add-responder", "addautoresponder"],
    usage="/add-auto-responder oi / ola",
    handle=handle,
)
