from __future__ import annotations

from takeshi_bot import config
from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext
from takeshi_bot.database import get_spider_api_token
from takeshi_bot.errors import DangerError


async def handle(ctx: CommandContext) -> None:
    import httpx

    token = get_spider_api_token()
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get(f"{config.SPIDER_API_BASE_URL}/saldo", params={"api_key": token})
        response.raise_for_status()
        data = response.json()
    if not data.get("success"):
        raise DangerError(f"Erro ao consultar saldo! {data.get('message', '')}")
    end_date = str(data.get("end_date", ""))
    parts = end_date.split("-")
    validity = f"{parts[2]}/{parts[1]}/{parts[0]}" if len(parts) == 3 else end_date
    await ctx.send_success_reply(
        "*Saldo da Spider X API*\n\n"
        f"*Plano:* {data.get('plan', '')}\n"
        f"*Requests restantes:* {data.get('requests_left', '')}\n"
        f"*Validade do plano:* {validity}"
    )


command = Command(
    name="saldo",
    description="Consulta saldo de requests da Spider X API.",
    commands=["saldo", "balance"],
    usage="/saldo",
    handle=handle,
)
