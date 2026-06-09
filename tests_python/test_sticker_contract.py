from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from typing import Any

import takeshi_bot.commands.member.rename as rename_command
from takeshi_bot.context import CommandContext


class FakeBridge:
    def __init__(self, sticker_path: str) -> None:
        self.sticker_path = sticker_path
        self.calls: list[tuple[str, Any]] = []

    async def send_presence(self, remote_jid: str, presence: str) -> None:
        self.calls.append(("send_presence", remote_jid, presence))

    async def send_message(self, remote_jid: str, content: dict[str, Any], options=None):
        self.calls.append(("send_message", remote_jid, content, options or {}))

    async def download_media(self, web_message, context, file_name, extension):
        self.calls.append(("download_media", context, file_name, extension))
        return self.sticker_path

    async def send_file_message(self, remote_jid, media_key, file_path, content=None, options=None):
        self.calls.append(("send_file_message", media_key, file_path, content or {}, options or {}))

    async def add_sticker_metadata(self, input_path, output_path, metadata):
        self.calls.append(("add_sticker_metadata", input_path, output_path, metadata))
        Path(output_path).write_bytes(Path(input_path).read_bytes())
        return output_path


class StickerContractTest(unittest.IsolatedAsyncioTestCase):
    async def test_rename_calls_bridge_metadata_with_pack_and_author(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            sticker = Path(tmp) / "sticker.webp"
            sticker.write_bytes(b"RIFF----WEBP")
            bridge = FakeBridge(str(sticker))
            web_message = {
                "key": {"remoteJid": "123@g.us", "participant": "user@lid"},
                "message": {"stickerMessage": {"mimetype": "image/webp"}},
            }
            ctx = CommandContext.from_web_message(bridge, web_message)
            assert ctx is not None
            ctx.args = ["Pacote", "Autor"]

            await rename_command.handle(ctx)

            metadata_calls = [call for call in bridge.calls if call[0] == "add_sticker_metadata"]
            self.assertEqual(len(metadata_calls), 1)
            self.assertEqual(metadata_calls[0][3]["packName"], "Pacote")
            self.assertEqual(metadata_calls[0][3]["packPublisher"], "Autor")


if __name__ == "__main__":
    unittest.main()
