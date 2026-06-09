from __future__ import annotations

from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext
from takeshi_bot.database import list_auto_responder_items


async def handle(ctx: CommandContext) -> None:
    await ctx.send_react("\u23f3")
    items = list_auto_responder_items()
    if not items:
        await ctx.send_success_reply("Nao ha termos cadastrados no auto-responder.")
        return
    lines = ["*Lista do auto-responder*", ""]
    for item in items:
        lines.append(f"{item.get('key')}. {item.get('match')}")
        lines.append(f"   -> \"{item.get('answer')}\"")
        lines.append("")
    lines.append(f"_Total: {len(items)} termo(s) cadastrado(s)_")
    await ctx.send_success_reply("\n".join(lines))


command = Command(
    name="list-auto-responder",
    description="Lista termos do auto-responder.",
    commands=["list-auto-responder", "list-auto", "list-responder"],
    usage="/list-auto-responder",
    handle=handle,
)
