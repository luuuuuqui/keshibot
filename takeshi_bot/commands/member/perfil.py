from __future__ import annotations

import random

from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext
from takeshi_bot.errors import InvalidParameterError
from takeshi_bot.paths import ASSETS_DIR
from takeshi_bot.utils import only_numbers


async def handle(ctx: CommandContext) -> None:
    if not ctx.is_group:
        raise InvalidParameterError("Este comando so pode ser usado em grupo.")
    target_lid = f"{only_numbers(ctx.args[0])}@lid" if ctx.args else ctx.user_lid
    await ctx.send_wait_reply("Carregando perfil...")
    participants = await ctx.get_group_participants()
    participant = next(
        (item for item in participants if item.get("id") == target_lid),
        None,
    )
    role = "Administrador" if participant and participant.get("admin") else "Membro"
    try:
        image_url = await ctx.bridge.profile_picture_url(target_lid)
    except Exception:
        image_url = str(ASSETS_DIR / "images" / "default-user.png")
    random_percent = random.randint(0, 99)
    program_price = random.uniform(1000, 6000)
    beauty = random.randint(1, 100)
    caption = (
        f"*Nome:* @{target_lid.split('@')[0]}\n"
        f"*Cargo:* {role}\n\n"
        f"*Programa:* R$ {program_price:.2f}\n"
        f"*Gado:* {random_percent + 7}%\n"
        f"*Passiva:* {random_percent + 5}%\n"
        f"*Beleza:* {beauty}%"
    )
    await ctx.send_react("\u2705")
    await ctx.bridge.send_message(
        ctx.remote_jid,
        {"image": {"url": image_url}, "caption": caption, "mentions": [target_lid]},
    )


command = Command(
    name="perfil",
    description="Mostra informacoes de um usuario.",
    commands=["perfil", "profile"],
    usage="/perfil ou /perfil @usuario",
    handle=handle,
)
