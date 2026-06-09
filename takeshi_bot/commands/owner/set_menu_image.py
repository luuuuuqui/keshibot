from __future__ import annotations

import shutil
from pathlib import Path

from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext
from takeshi_bot.errors import InvalidParameterError
from takeshi_bot.paths import ASSETS_DIR


async def handle(ctx: CommandContext) -> None:
    if not ctx.is_reply or not ctx.is_image:
        raise InvalidParameterError("Voce precisa responder a uma mensagem que contenha imagem!")
    menu_image = ASSETS_DIR / "images" / "takeshi-bot.png"
    backup = ASSETS_DIR / "images" / "takeshi-bot-backup.png"
    temp_path = await ctx.download_image("new-menu-image-temp")
    if not temp_path:
        raise RuntimeError("Nao consegui baixar a imagem.")
    if menu_image.exists():
        shutil.copyfile(menu_image, backup)
    Path(temp_path).replace(menu_image)
    await ctx.send_success_reply("Imagem do menu atualizada com sucesso!")


command = Command(
    name="set-menu-image",
    description="Altera a imagem do menu do bot.",
    commands=[
        "set-menu-image",
        "set-image",
        "set-imagem-menu",
        "set-img-menu",
        "set-menu-imagem",
        "set-menu-img",
    ],
    usage="/set-menu-image",
    handle=handle,
)
