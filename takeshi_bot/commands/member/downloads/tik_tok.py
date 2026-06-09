from __future__ import annotations

from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext
from ._helpers import send_download_video


async def handle(ctx: CommandContext) -> None:
    await send_download_video(ctx, "tik-tok", "tiktok.com")


command = Command(
    name="tik-tok",
    description="Baixa videos do TikTok.",
    commands=["tik-tok", "tiktok", "ttk"],
    usage="/tik-tok https://tiktok.com/...",
    handle=handle,
)
