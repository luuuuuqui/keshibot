from __future__ import annotations

from pathlib import Path

from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext
from takeshi_bot.errors import DangerError, InvalidParameterError
from takeshi_bot.paths import ASSETS_DIR
from takeshi_bot.utils import only_numbers


def make_action_command(
    name: str,
    aliases: list[str],
    description: str,
    asset_name: str,
    verb_message: str,
) -> Command:
    async def handle(ctx: CommandContext) -> None:
        if not ctx.args and not ctx.is_reply:
            raise InvalidParameterError("Voce precisa mencionar ou marcar um membro!")
        target_lid = ctx.reply_lid if ctx.is_reply else f"{only_numbers(ctx.args[0])}@lid"
        if not target_lid:
            await ctx.send_error_reply("Voce precisa mencionar um usuario ou responder uma mensagem.")
            return
        user_number = only_numbers(ctx.user_lid)
        target_number = only_numbers(target_lid)
        asset_path = ASSETS_DIR / "images" / "funny" / asset_name
        if not asset_path.exists():
            await ctx.send_reply(verb_message.format(user=user_number, target=target_number), [ctx.user_lid, target_lid])
            return
        await ctx.send_gif_from_file(
            str(asset_path),
            verb_message.format(user=user_number, target=target_number),
            [ctx.user_lid, target_lid],
        )

    return Command(name=name, description=description, commands=aliases, usage=f"/{name} @usuario", handle=handle)


async def dice_handle(ctx: CommandContext) -> None:
    import random

    if not ctx.args:
        raise DangerError("Por favor, escolha um numero entre 1 e 6! Exemplo: /dado 3")
    try:
        number = int(ctx.args[0])
    except ValueError as error:
        raise DangerError("Por favor, escolha um numero entre 1 e 6! Exemplo: /dado 3") from error
    if number < 1 or number > 6:
        raise DangerError("Por favor, escolha um numero entre 1 e 6! Exemplo: /dado 3")
    await ctx.send_wait_reply("Rolando o dado...")
    result = random.randint(1, 6)
    sticker = ASSETS_DIR / "stickers" / "dice" / f"{result}.webp"
    if sticker.exists():
        await ctx.send_sticker_from_file(str(sticker))
    if number == result:
        await ctx.send_react("\U0001f3c6")
        await ctx.send_reply(f"Voce ganhou! Apostou {number} e o dado caiu em {result}.")
    else:
        await ctx.send_react("\U0001f622")
        await ctx.send_reply(f"Voce perdeu. Apostou {number}, mas o dado caiu em {result}.")
