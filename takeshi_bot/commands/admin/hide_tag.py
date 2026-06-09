from __future__ import annotations

from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext


async def handle(ctx: CommandContext) -> None:
    metadata = await ctx.bridge.group_metadata(ctx.remote_jid)
    mentions = [participant.get("id") for participant in metadata.get("participants", [])]
    mentions = [mention for mention in mentions if mention]
    await ctx.send_react("\U0001f4e2")
    await ctx.send_text(f"\U0001f4e2 Marcando todos!\n\n{ctx.full_args}", mentions)


command = Command(
    name="hide-tag",
    description="Marca todos do grupo sem listar nomes.",
    commands=["hide-tag", "to-tag", "marcar", "marca", "tag-all"],
    usage="/hide-tag motivo",
    handle=handle,
)
