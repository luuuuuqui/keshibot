from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from typing import Any

import takeshi_bot.config as config
import takeshi_bot.database as database
from takeshi_bot.context import CommandContext
from takeshi_bot.dynamic_command import dynamic_command


class FakeBridge:
    def __init__(self) -> None:
        self.calls: list[tuple[str, Any]] = []

    async def send_presence(self, remote_jid: str, presence: str) -> None:
        self.calls.append(("send_presence", remote_jid, presence))

    async def send_message(
        self,
        remote_jid: str,
        content: dict[str, Any],
        options: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        self.calls.append(("send_message", remote_jid, content, options or {}))
        return {"ok": True}

    async def group_metadata(self, remote_jid: str) -> dict[str, Any]:
        self.calls.append(("group_metadata", remote_jid))
        return {
            "participants": [
                {"id": config.OWNER_LID, "admin": "admin"},
                {"id": "admin@lid", "admin": "admin"},
            ]
        }

    async def group_participants_update(
        self, remote_jid: str, participants: list[str], operation: str
    ) -> None:
        self.calls.append(("group_participants_update", remote_jid, participants, operation))

    async def delete_message(self, remote_jid: str, key: dict[str, Any]) -> None:
        self.calls.append(("delete_message", remote_jid, key))

    async def group_setting_update(self, remote_jid: str, setting: str) -> None:
        self.calls.append(("group_setting_update", remote_jid, setting))

    async def add_sticker_metadata(
        self, input_path: str, output_path: str, metadata: dict[str, Any]
    ) -> str:
        self.calls.append(("add_sticker_metadata", input_path, output_path, metadata))
        return output_path


def make_context(text: str, user_lid: str = config.OWNER_LID) -> CommandContext:
    web_message = {
        "key": {
            "remoteJid": "123@g.us",
            "participant": user_lid,
            "id": "ABC",
        },
        "message": {"conversation": text},
    }
    ctx = CommandContext.from_web_message(FakeBridge(), web_message, 1.0)
    assert ctx is not None
    return ctx


class DynamicCommandTest(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.original_dir = database.DATABASE_DIR
        database.DATABASE_DIR = Path(self.temp.name)

    def tearDown(self) -> None:
        database.DATABASE_DIR = self.original_dir
        self.temp.cleanup()

    async def test_ping_command_sends_reply(self) -> None:
        ctx = make_context("/ping")
        await dynamic_command(ctx)

        sent = [call for call in ctx.bridge.calls if call[0] == "send_message"]
        self.assertTrue(any("Pong!" in call[2].get("text", "") for call in sent))

    async def test_prefix_lookup_reply_without_command(self) -> None:
        ctx = make_context("qual o prefixo?")
        await dynamic_command(ctx)

        sent = [call for call in ctx.bridge.calls if call[0] == "send_message"]
        self.assertTrue(any("O padrao e: /" in call[2].get("text", "") for call in sent))

    async def test_set_prefix_changes_runtime_database(self) -> None:
        ctx = make_context("/set-prefix !")
        await dynamic_command(ctx)

        self.assertEqual(database.get_prefix("123@g.us"), "!")

    async def test_anti_link_removes_non_admin_member(self) -> None:
        database.activate_anti_link_group("123@g.us")
        ctx = make_context("https://example.com", user_lid="member@lid")
        await dynamic_command(ctx)

        self.assertTrue(
            any(call[0] == "group_participants_update" for call in ctx.bridge.calls)
        )
        self.assertTrue(any(call[0] == "delete_message" for call in ctx.bridge.calls))

    async def test_welcome_command_toggles_database(self) -> None:
        ctx = make_context("/welcome 1", user_lid="admin@lid")
        await dynamic_command(ctx)

        self.assertTrue(database.is_active_welcome_group("123@g.us"))

    async def test_warn_removes_member_at_limit(self) -> None:
        ctx = make_context("/warn @555 motivo", user_lid="admin@lid")
        await dynamic_command(ctx)
        await dynamic_command(make_context("/warn @555 motivo", user_lid="admin@lid"))
        third = make_context("/warn @555 motivo", user_lid="admin@lid")
        await dynamic_command(third)

        self.assertTrue(
            any(call[0] == "group_participants_update" for call in third.bridge.calls)
        )


if __name__ == "__main__":
    unittest.main()
