from __future__ import annotations

from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext
from ._helpers import send_download_video


async def handle(ctx: CommandContext) -> None:
    await send_download_video(ctx, "facebook", "facebook.com")


command = Command(
    name="facebook",
    description="Baixa videos do Facebook.",
    commands=["facebook", "fb"],
    usage="/facebook https://facebook.com/...",
    handle=handle,
)
