from __future__ import annotations

import re

from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext
from takeshi_bot.errors import InvalidParameterError


async def handle(ctx: CommandContext) -> None:
    cep = ctx.args[0] if ctx.args else ""
    digits = re.sub(r"[^0-9]", "", cep)
    if len(digits) != 8:
        raise InvalidParameterError("Voce precisa enviar um CEP no formato 00000-000!")

    import httpx

    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.get(f"https://viacep.com.br/ws/{digits}/json/")
        response.raise_for_status()
        data = response.json()

    if data.get("erro"):
        await ctx.send_warning_reply("CEP nao encontrado!")
        return

    await ctx.send_success_reply(
        "*Resultado*\n\n"
        f"*CEP*: {data.get('cep', '')}\n"
        f"*Logradouro*: {data.get('logradouro', '')}\n"
        f"*Complemento*: {data.get('complemento', '')}\n"
        f"*Bairro*: {data.get('bairro', '')}\n"
        f"*Localidade*: {data.get('localidade', '')}\n"
        f"*UF*: {data.get('uf', '')}\n"
        f"*IBGE*: {data.get('ibge', '')}"
    )


command = Command(
    name="cep",
    description="Consulta CEP.",
    commands=["cep"],
    usage="/cep 01001-001",
    handle=handle,
)
