from __future__ import annotations

from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext
from ._helpers import send_download_video


async def handle(ctx: CommandContext) -> None:
    await send_download_video(ctx, "instagram", "instagram.com")


command = Command(
    name="instagram",
    description="Baixa videos/reels do Instagram.",
    commands=["instagram", "ig", "inst", "insta"],
    usage="/instagram https://www.instagram.com/reel/...",
    handle=handle,
)
