from __future__ import annotations

import unittest
from pathlib import Path
from unittest.mock import AsyncMock, patch

import takeshi_bot.commands.member.ia.ia_sticker as ia_sticker


class FakeContext:
    def __init__(self) -> None:
        self.full_args = "gato astronauta"
        self.calls: list[tuple[str, object]] = []

    async def send_wait_reply(self, text: str = "") -> None:
        self.calls.append(("send_wait_reply", text))

    async def send_warning_reply(self, text: str) -> None:
        self.calls.append(("send_warning_reply", text))

    async def send_react(self, emoji: str) -> None:
        self.calls.append(("send_react", emoji))

    async def send_sticker_from_file(self, file_path: str) -> None:
        self.calls.append(("send_sticker_from_file", file_path))


class FakeFfmpeg:
    async def execute(self, *args: str) -> None:
        Path(args[-1]).write_bytes(b"WEBP")


class IaStickerTest(unittest.IsolatedAsyncioTestCase):
    async def test_ia_sticker_converts_image_url_to_local_webp_sticker(self) -> None:
        ctx = FakeContext()
        with (
            patch.object(ia_sticker, "image_ai", AsyncMock(return_value={"image": "https://example.test/image.png"})),
            patch.object(ia_sticker, "_download_image", AsyncMock(return_value=b"PNG")),
            patch.object(ia_sticker, "Ffmpeg", return_value=FakeFfmpeg()),
        ):
            await ia_sticker.handle(ctx)  # type: ignore[arg-type]

        sticker_calls = [call for call in ctx.calls if call[0] == "send_sticker_from_file"]
        self.assertEqual(len(sticker_calls), 1)
        self.assertTrue(str(sticker_calls[0][1]).endswith(".webp"))
        self.assertFalse(Path(sticker_calls[0][1]).exists())
        self.assertIn(("send_react", "\u2705"), ctx.calls)


if __name__ == "__main__":
    unittest.main()
