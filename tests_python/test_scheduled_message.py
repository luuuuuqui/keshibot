from __future__ import annotations

import asyncio
import unittest
from typing import Any
from unittest.mock import patch

from takeshi_bot.commands.admin import agendar_mensagem
from takeshi_bot.context import CommandContext


class FakeBridge:
    def __init__(self) -> None:
        self.calls: list[tuple[str, Any]] = []

    async def send_presence(self, remote_jid: str, presence: str) -> None:
        self.calls.append(("send_presence", remote_jid, presence))

    async def send_message(self, remote_jid: str, content: dict[str, Any], options=None):
        self.calls.append(("send_message", remote_jid, content, options or {}))
        return {"key": {"id": "MSG"}}


def make_context(args: list[str]) -> CommandContext:
    web_message = {
        "key": {"remoteJid": "123@g.us", "participant": "admin@lid"},
        "message": {"conversation": "/agendar-mensagem"},
    }
    ctx = CommandContext.from_web_message(FakeBridge(), web_message)
    assert ctx is not None
    ctx.args = args
    return ctx


class ScheduledMessageTest(unittest.IsolatedAsyncioTestCase):
    async def test_sends_scheduled_message_after_delay(self) -> None:
        ctx = make_context(["Reuniao amanha", "10s"])
        original_sleep = asyncio.sleep
        sleeps: list[float] = []

        async def immediate_sleep(seconds: float) -> None:
            sleeps.append(seconds)
            await original_sleep(0)

        with patch.object(agendar_mensagem.asyncio, "sleep", immediate_sleep):
            await agendar_mensagem.handle(ctx)
            for _ in range(5):
                await original_sleep(0)

        texts = [
            call[2]["text"]
            for call in ctx.bridge.calls
            if call[0] == "send_message" and "text" in call[2]
        ]
        self.assertIn(10, sleeps)
        self.assertTrue(any("Mensagem agendada para daqui a 10s" in text for text in texts))
        self.assertTrue(any("*Mensagem agendada:*\n\nReuniao amanha" in text for text in texts))

    async def test_rejects_invalid_argument_count(self) -> None:
        ctx = make_context(["Reuniao amanha"])

        await agendar_mensagem.handle(ctx)

        texts = [
            call[2]["text"]
            for call in ctx.bridge.calls
            if call[0] == "send_message" and "text" in call[2]
        ]
        self.assertTrue(any("Formato incorreto" in text for text in texts))

    async def test_rejects_invalid_time_unit(self) -> None:
        ctx = make_context(["Reuniao amanha", "10d"])

        await agendar_mensagem.handle(ctx)

        texts = [
            call[2]["text"]
            for call in ctx.bridge.calls
            if call[0] == "send_message" and "text" in call[2]
        ]
        self.assertTrue(any("Formato de tempo invalido" in text for text in texts))


if __name__ == "__main__":
    unittest.main()
