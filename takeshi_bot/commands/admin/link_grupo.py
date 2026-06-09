from __future__ import annotations

from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext
from takeshi_bot.errors import DangerError


async def handle(ctx: CommandContext) -> None:
    code = await ctx.bridge.group_invite_code(ctx.remote_jid)
    if not code:
        raise DangerError("Preciso ser admin!")
    await ctx.send_react("\U0001fa80")
    await ctx.send_reply(f"https://chat.whatsapp.com/{code}")


command = Command(
    name="link-grupo",
    description="Obtem o link do grupo.",
    commands=["link-grupo", "link-gp"],
    usage="/link-grupo",
    handle=handle,
)
