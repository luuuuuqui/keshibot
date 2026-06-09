from __future__ import annotations

import asyncio
import re

from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext


def _parse_time(raw_time: str) -> float | None:
    if not re.fullmatch(r"\d+[smh]", raw_time):
        return None
    value = int(raw_time[:-1])
    unit = raw_time[-1]
    if unit == "s":
        return value
    if unit == "m":
        return value * 60
    return value * 60 * 60


async def handle(ctx: CommandContext) -> None:
    if len(ctx.args) != 2:
        await ctx.send_error_reply("Formato incorreto. Use: /agendar-mensagem mensagem / tempo")
        return
    message = ctx.args[0].strip()
    raw_time = ctx.args[1].strip()
    seconds = _parse_time(raw_time)
    if not message or not seconds:
        await ctx.send_error_reply("Mensagem invalida ou tempo nao especificado corretamente.")
        return
    await ctx.send_success_reply(f"Mensagem agendada para daqui a {raw_time}...")

    async def send_later() -> None:
        await asyncio.sleep(seconds)
        await ctx.send_text(f"*Mensagem agendada:*\n\n{message}")

    asyncio.create_task(send_later())


command = Command(
    name="agendar-mensagem",
    description="Agenda uma mensagem para envio posterior.",
    commands=["agendar", "agendar-mensagem"],
    usage="/agendar-mensagem mensagem / 10m",
    handle=handle,
)
