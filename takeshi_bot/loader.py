from __future__ import annotations

import asyncio
import time
from typing import Any

from takeshi_bot import config
from takeshi_bot.bridge import BaileysBridge, BridgeEvent
from takeshi_bot.context import CommandContext
from takeshi_bot.database import check_if_member_is_muted
from takeshi_bot.dynamic_command import dynamic_command
from takeshi_bot.logger import error_log, info_log
from takeshi_bot.message_handler import message_handler
from takeshi_bot.participants import on_group_participants_update
from takeshi_bot.stealth_payment import handle_stealth_payment_detection
from takeshi_bot.utils import only_numbers


async def _ask_input(prompt: str) -> str:
    return await asyncio.to_thread(input, prompt)


async def on_messages_upsert(bridge: BaileysBridge, messages: list[dict[str, Any]]) -> None:
    if not messages:
        return

    start_process = time.time()
    await asyncio.sleep(config.TIMEOUT_IN_MILLISECONDS_BY_EVENT / 1000)

    for web_message in messages:
        try:
            key = web_message.get("key") or {}
            await handle_stealth_payment_detection(bridge, web_message)
            participant = (key.get("participant") or "").split(":")[0]
            if check_if_member_is_muted(key.get("remoteJid"), participant):
                await bridge.delete_message(
                    key.get("remoteJid"),
                    {
                        "remoteJid": key.get("remoteJid"),
                        "fromMe": False,
                        "id": key.get("id"),
                        "participant": key.get("participant"),
                    },
                )
                return

            if web_message.get("message"):
                await message_handler(bridge, web_message)

            stub_type = web_message.get("messageStubType")
            if stub_type in {27, 28, "GROUP_PARTICIPANT_ADD", "GROUP_PARTICIPANT_LEAVE"}:
                action = "add" if stub_type in {27, "GROUP_PARTICIPANT_ADD"} else "remove"
                await on_group_participants_update(
                    bridge,
                    key.get("remoteJid") or "",
                    web_message.get("messageStubParameters") or [],
                    action,
                )
                return

            ctx = CommandContext.from_web_message(bridge, web_message, start_process)
            if ctx is None:
                continue
            await dynamic_command(ctx)
        except Exception as error:  # noqa: BLE001 - event boundary
            error_log(f"Erro ao processar mensagem: {error}", error)


async def handle_event(bridge: BaileysBridge, event: BridgeEvent) -> None:
    if event.type == "messages.upsert":
        await on_messages_upsert(bridge, event.payload.get("messages") or [])
    elif event.type == "connection.update":
        connection = event.payload.get("connection")
        if connection:
            info_log(f"Conexao WhatsApp: {connection}")
    elif event.type == "sidecar.ready":
        if not event.payload.get("registered"):
            phone_number = await _ask_input(
                'Informe o numero do bot (ex: "+5511912345678"): '
            )
            result = await bridge.request(
                "request_pairing_code", {"phoneNumber": only_numbers(phone_number)}
            )
            info_log(f"Codigo de pareamento: {result.get('formattedCode')}")
    elif event.type == "sidecar.error":
        error_log(f"Sidecar error: {event.payload}")


async def load(bridge: BaileysBridge) -> None:
    async for event in bridge.events():
        await handle_event(bridge, event)
