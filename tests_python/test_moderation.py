from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from typing import Any

import takeshi_bot.database as database
from takeshi_bot.message_handler import message_handler
from takeshi_bot.participants import on_group_participants_update
from takeshi_bot.stealth_payment import handle_stealth_payment_detection, tracker


class FakeBridge:
    def __init__(self) -> None:
        self.calls: list[tuple[str, Any]] = []

    async def send_message(self, remote_jid: str, content: dict[str, Any], options=None):
        self.calls.append(("send_message", remote_jid, content, options or {}))

    async def delete_message(self, remote_jid: str, key: dict[str, Any]):
        self.calls.append(("delete_message", remote_jid, key))

    async def group_participants_update(
        self, remote_jid: str, participants: list[str], operation: str
    ):
        self.calls.append(("group_participants_update", remote_jid, participants, operation))

    async def group_setting_update(self, remote_jid: str, setting: str):
        self.calls.append(("group_setting_update", remote_jid, setting))

    async def group_metadata(self, remote_jid: str):
        self.calls.append(("group_metadata", remote_jid))
        return {"participants": [{"id": "admin@lid", "admin": "admin"}]}

    async def request(self, action: str, payload: dict[str, Any] | None = None):
        self.calls.append(("request", action, payload or {}))
        if action == "profile_picture_url":
            return "https://example.com/profile.jpg"
        return None


class ModerationTest(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.original_dir = database.DATABASE_DIR
        database.DATABASE_DIR = Path(self.temp.name)
        database.write_json(
            "restricted-messages",
            {
                "image": "imageMessage",
                "product": "productMessage",
                "event": "eventMessage",
                "lottieSticker": "lottieStickerMessage",
            },
        )

    def tearDown(self) -> None:
        database.DATABASE_DIR = self.original_dir
        self.temp.cleanup()

    async def test_restricted_image_is_deleted(self) -> None:
        bridge = FakeBridge()
        database.update_is_active_group_restriction("123@g.us", "anti-image", True)
        await message_handler(
            bridge,
            {
                "key": {
                    "remoteJid": "123@g.us",
                    "participant": "member@lid",
                    "id": "IMG",
                    "fromMe": False,
                },
                "message": {"imageMessage": {"caption": "x"}},
            },
        )

        self.assertTrue(any(call[0] == "delete_message" for call in bridge.calls))

    async def test_restricted_product_event_and_lottie_are_deleted(self) -> None:
        cases = [
            ("anti-product", {"productMessage": {"title": "Oferta"}}),
            ("anti-event", {"eventMessage": {"name": "Evento"}}),
            ("anti-lottieSticker", {"lottieStickerMessage": {"mimetype": "application/lottie+json"}}),
        ]
        for restriction, message in cases:
            with self.subTest(restriction=restriction):
                bridge = FakeBridge()
                database.update_is_active_group_restriction("123@g.us", restriction, True)
                await message_handler(
                    bridge,
                    {
                        "key": {
                            "remoteJid": "123@g.us",
                            "participant": "member@lid",
                            "id": restriction,
                            "fromMe": False,
                        },
                        "message": message,
                    },
                )

                self.assertTrue(any(call[0] == "delete_message" for call in bridge.calls))

    async def test_welcome_participant_message(self) -> None:
        bridge = FakeBridge()
        database.activate_welcome_group("123@g.us")
        await on_group_participants_update(bridge, "123@g.us", ["999@lid"], "add")

        sent = [call for call in bridge.calls if call[0] == "send_message"]
        self.assertTrue(sent)
        self.assertIn("@999", sent[0][2]["caption"])
        self.assertEqual(sent[0][2]["image"]["url"], "https://example.com/profile.jpg")

    async def test_stealth_payment_removes_sender(self) -> None:
        tracker.clear()
        bridge = FakeBridge()
        database.update_is_active_group_restriction("123@g.us", "anti-payment", True)
        await handle_stealth_payment_detection(
            bridge,
            {
                "key": {
                    "remoteJid": "123@g.us",
                    "participant": "member@lid",
                    "fromMe": False,
                },
                "messageStubType": 2,
                "stealthMeta": {"decryptFail": "hide"},
            },
        )

        self.assertTrue(
            any(call == ("group_setting_update", "123@g.us", "announcement") for call in bridge.calls)
        )
        self.assertTrue(
            any(call[0] == "group_participants_update" and call[3] == "remove" for call in bridge.calls)
        )
        self.assertTrue(
            any(
                call[0] == "send_message"
                and "Anti-Payment (Stealth)" in call[2].get("text", "")
                for call in bridge.calls
            )
        )


if __name__ == "__main__":
    unittest.main()
