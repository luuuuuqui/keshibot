from __future__ import annotations

import unittest
from typing import Any

from takeshi_bot.commands.member.exemplos.enviar_botoes import command as buttons_command
from takeshi_bot.commands.member.exemplos.enviar_carrossel import (
    command as carousel_command,
)
from takeshi_bot.commands.member.exemplos.enviar_documento_de_arquivo import (
    command as document_command,
)
from takeshi_bot.commands.member.exemplos.enviar_enquete import command as poll_command
from takeshi_bot.commands.member.exemplos.enviar_imagem_de_arquivo import (
    command as image_command,
)
from takeshi_bot.commands.member.exemplos.enviar_lista import command as list_command
from takeshi_bot.context import CommandContext


class FakeBridge:
    def __init__(self) -> None:
        self.calls: list[tuple[str, Any]] = []

    async def send_presence(self, remote_jid: str, presence: str) -> None:
        self.calls.append(("send_presence", remote_jid, presence))

    async def send_message(self, remote_jid: str, content: dict[str, Any], options=None):
        self.calls.append(("send_message", remote_jid, content, options or {}))
        return {"key": {"id": "MSG"}}

    async def send_file_message(self, remote_jid, media_key, file_path, content=None, options=None):
        self.calls.append(("send_file_message", media_key, file_path, content or {}, options or {}))
        return {"key": {"id": "FILE"}}


def make_context() -> CommandContext:
    web_message = {
        "key": {"remoteJid": "123@g.us", "participant": "user@lid"},
        "message": {"conversation": "/example"},
    }
    ctx = CommandContext.from_web_message(FakeBridge(), web_message)
    assert ctx is not None
    return ctx


class ExamplesTest(unittest.IsolatedAsyncioTestCase):
    async def test_buttons_example_sends_buttons_payload(self) -> None:
        ctx = make_context()
        await buttons_command.handle(ctx)
        messages = [call for call in ctx.bridge.calls if call[0] == "send_message"]
        self.assertTrue(messages)
        self.assertTrue(any("buttons" in message[2] for message in messages))
        self.assertTrue(any("interactiveButtons" in message[2] for message in messages))

    async def test_list_example_sends_sections_with_trigger_ids(self) -> None:
        ctx = make_context()
        await list_command.handle(ctx)
        messages = [call for call in ctx.bridge.calls if call[0] == "send_message"]
        content = messages[-1][2]
        self.assertIn("sections", content)
        self.assertTrue(content["viewOnce"])
        first_row = content["sections"][0]["rows"][0]
        self.assertEqual(first_row["rowId"], "/exemplo-gatilho texto")

    async def test_carousel_example_sends_remote_cards(self) -> None:
        ctx = make_context()
        await carousel_command.handle(ctx)
        messages = [call for call in ctx.bridge.calls if call[0] == "send_message"]
        content = messages[-1][2]
        self.assertEqual(len(content["cards"]), 3)
        self.assertTrue(content["viewOnce"])
        self.assertTrue(content["cards"][0]["image"]["url"].startswith("https://"))

    async def test_poll_example_sends_poll_payload(self) -> None:
        ctx = make_context()
        await poll_command.handle(ctx)
        messages = [call for call in ctx.bridge.calls if call[0] == "send_message"]
        self.assertIn("poll", messages[-1][2])

    async def test_document_example_sends_document_file(self) -> None:
        ctx = make_context()
        await document_command.handle(ctx)
        files = [call for call in ctx.bridge.calls if call[0] == "send_file_message"]
        self.assertTrue(files)
        self.assertEqual(files[-1][1], "document")

    async def test_image_example_sends_image_file(self) -> None:
        ctx = make_context()
        await image_command.handle(ctx)
        files = [call for call in ctx.bridge.calls if call[0] == "send_file_message"]
        self.assertTrue(files)
        self.assertEqual(files[-1][1], "image")


if __name__ == "__main__":
    unittest.main()
