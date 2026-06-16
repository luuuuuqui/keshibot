from __future__ import annotations

import unittest
from typing import Any

from takeshi_bot.commands.admin import link_grupo, set_name
from takeshi_bot.context import CommandContext


class FakeBridge:
    def __init__(self) -> None:
        self.calls: list[tuple[str, Any]] = []
        self.invite_code: str | None = "ABC123"
        self.fail_invite = False
        self.fail_subject = False

    async def send_presence(self, remote_jid: str, presence: str) -> None:
        self.calls.append(("send_presence", remote_jid, presence))

    async def send_message(self, remote_jid: str, content: dict[str, Any], options=None):
        self.calls.append(("send_message", remote_jid, content, options or {}))
        return {"key": {"id": "MSG"}}

    async def group_invite_code(self, remote_jid: str) -> str | None:
        self.calls.append(("group_invite_code", remote_jid))
        if self.fail_invite:
            raise RuntimeError("not admin")
        return self.invite_code

    async def group_metadata(self, remote_jid: str) -> dict[str, Any]:
        self.calls.append(("group_metadata", remote_jid))
        return {"subject": "Nome antigo", "participants": []}

    async def group_update_subject(self, remote_jid: str, subject: str) -> None:
        self.calls.append(("group_update_subject", remote_jid, subject))
        if self.fail_subject:
            raise RuntimeError("not admin")


def make_context(text: str = "/cmd", bridge: FakeBridge | None = None) -> CommandContext:
    web_message = {
        "key": {"remoteJid": "123@g.us", "participant": "admin@lid"},
        "message": {"conversation": text},
    }
    ctx = CommandContext.from_web_message(bridge or FakeBridge(), web_message)
    assert ctx is not None
    return ctx


def sent_texts(ctx: CommandContext) -> list[str]:
    return [
        call[2]["text"]
        for call in ctx.bridge.calls
        if call[0] == "send_message" and "text" in call[2]
    ]


class AdminGroupCommandsTest(unittest.IsolatedAsyncioTestCase):
    async def test_link_grupo_sends_invite_link(self) -> None:
        ctx = make_context()

        await link_grupo.handle(ctx)

        self.assertTrue(any("https://chat.whatsapp.com/ABC123" in text for text in sent_texts(ctx)))

    async def test_link_grupo_handles_missing_admin_permission(self) -> None:
        bridge = FakeBridge()
        bridge.fail_invite = True
        ctx = make_context(bridge=bridge)

        await link_grupo.handle(ctx)

        self.assertTrue(any("Preciso ser admin" in text for text in sent_texts(ctx)))

    async def test_set_name_reports_old_and_new_group_names(self) -> None:
        ctx = make_context("/set-name Novo nome")
        ctx.full_args = "Novo nome"

        await set_name.handle(ctx)

        self.assertTrue(any("*Antigo*: Nome antigo" in text for text in sent_texts(ctx)))
        self.assertTrue(any("*Novo*: Novo nome" in text for text in sent_texts(ctx)))

    async def test_set_name_handles_missing_admin_permission(self) -> None:
        bridge = FakeBridge()
        bridge.fail_subject = True
        ctx = make_context("/set-name Novo nome", bridge)
        ctx.full_args = "Novo nome"

        await set_name.handle(ctx)

        self.assertTrue(any("Falha ao alterar o nome do grupo" in text for text in sent_texts(ctx)))


if __name__ == "__main__":
    unittest.main()
