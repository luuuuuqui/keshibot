from __future__ import annotations

from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext
from takeshi_bot.errors import InvalidParameterError
from takeshi_bot.services.sticker import create_sticker


async def handle(ctx: CommandContext) -> None:
    if not ctx.is_image and not ctx.is_video:
        raise InvalidParameterError(
            "Voce precisa marcar ou responder a uma imagem/gif/video!"
        )
    await ctx.send_react("\u23f3")
    await create_sticker(ctx)
    await ctx.send_react("\u2705")


command = Command(
    name="sticker",
    description="Cria figurinhas de imagem, gif ou video.",
    commands=["f", "s", "sticker", "fig"],
    usage="/sticker",
    handle=handle,
)
