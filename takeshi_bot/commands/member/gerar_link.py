from __future__ import annotations

from pathlib import Path

from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext
from takeshi_bot.errors import InvalidParameterError
from takeshi_bot.services.linker import upload
from takeshi_bot.utils import random_name, remove_file_if_exists


async def handle(ctx: CommandContext) -> None:
    if not ctx.is_image:
        raise InvalidParameterError("Voce deve marcar ou responder uma imagem!")
    await ctx.send_react("\u23f3")
    file_path = await ctx.download_image(random_name("upload"))
    try:
        if not file_path:
            raise RuntimeError("Nao consegui baixar a imagem.")
        link = await upload(Path(file_path).read_bytes(), Path(file_path).name)
        await ctx.send_react("\u2705")
        await ctx.send_reply(f"Aqui esta o link da sua imagem!\n\n- {link}")
    finally:
        remove_file_if_exists(file_path)


command = Command(
    name="gerar-link",
    description="Faz upload de imagem e retorna link.",
    commands=["to-link", "up", "upload", "gera-link", "gerar-link"],
    usage="/gerar-link",
    handle=handle,
)
