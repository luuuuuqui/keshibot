from __future__ import annotations

from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext
from takeshi_bot.errors import DangerError, InvalidParameterError
from takeshi_bot.paths import TEMP_DIR
from takeshi_bot.utils import random_name, remove_file_if_exists


async def handle(ctx: CommandContext) -> None:
    if not ctx.is_sticker:
        raise InvalidParameterError("Voce precisa responder a uma figurinha!")
    if len(ctx.args) != 2:
        raise InvalidParameterError("Voce precisa fornecer pacote e autor: pacote / autor")
    pack, author = ctx.args
    if len(pack) < 2 or len(pack) > 50:
        raise DangerError("O pacote deve ter entre 2 e 50 caracteres.")
    if len(author) < 2 or len(author) > 50:
        raise DangerError("O autor deve ter entre 2 e 50 caracteres.")
    await ctx.send_react("\u23f3")
    sticker_path = await ctx.download_sticker(random_name("webp"))
    renamed_path = str(TEMP_DIR / random_name("webp"))
    try:
        if not sticker_path:
            raise RuntimeError("Nao consegui baixar a figurinha.")
        await ctx.bridge.add_sticker_metadata(
            sticker_path,
            renamed_path,
            {"packName": pack, "packPublisher": author},
        )
        await ctx.send_sticker_from_file(renamed_path)
        await ctx.send_react("\u2705")
    finally:
        remove_file_if_exists(sticker_path)
        remove_file_if_exists(renamed_path)


command = Command(
    name="rename",
    description="Adiciona novos metadados a figurinha.",
    commands=["rename", "renomear", "rn"],
    usage="/rename pacote / autor",
    handle=handle,
)
