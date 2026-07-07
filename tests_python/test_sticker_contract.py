from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from typing import Any

import takeshi_bot.commands.member.rename as rename_command
import takeshi_bot.services.sticker as sticker_service
from takeshi_bot.context import CommandContext
from takeshi_bot.errors import InvalidParameterError


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


class FakeFfmpeg:
    async def execute(self, *args: str) -> None:
        Path(args[-1]).write_bytes(b"RIFF----WEBP")

    async def cleanup(self, file_path: str | None) -> None:
        if file_path:
            Path(file_path).unlink(missing_ok=True)


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

    async def test_create_sticker_rejects_direct_video_longer_than_js_limit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            video = Path(tmp) / "video.mp4"
            video.write_bytes(b"video")
            bridge = FakeBridge(str(video))
            web_message = {
                "key": {"remoteJid": "123@g.us", "participant": "user@lid"},
                "message": {"videoMessage": {"seconds": 11}},
            }
            ctx = CommandContext.from_web_message(bridge, web_message)
            assert ctx is not None

            with self.assertRaisesRegex(InvalidParameterError, "mais de 10 segundos"):
                await sticker_service.create_sticker(ctx)

            self.assertFalse(
                any(call[0] == "download_media" for call in bridge.calls),
                "videos too long should be rejected before downloading media",
            )

    async def test_create_sticker_rejects_quoted_video_longer_than_js_limit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            video = Path(tmp) / "video.mp4"
            video.write_bytes(b"video")
            bridge = FakeBridge(str(video))
            web_message = {
                "key": {"remoteJid": "123@g.us", "participant": "user@lid"},
                "message": {
                    "extendedTextMessage": {
                        "text": "/sticker",
                        "contextInfo": {
                            "quotedMessage": {"videoMessage": {"seconds": 42}}
                        },
                    }
                },
            }
            ctx = CommandContext.from_web_message(bridge, web_message)
            assert ctx is not None

            with self.assertRaisesRegex(InvalidParameterError, "mais de 10 segundos"):
                await sticker_service.create_sticker(ctx)

            self.assertFalse(any(call[0] == "download_media" for call in bridge.calls))

    async def test_create_sticker_accepts_video_within_js_limit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            video = Path(tmp) / "video.mp4"
            video.write_bytes(b"video")
            bridge = FakeBridge(str(video))
            web_message = {
                "key": {"remoteJid": "123@g.us", "participant": "user@lid"},
                "message": {"videoMessage": {"seconds": 10}},
            }
            ctx = CommandContext.from_web_message(bridge, web_message)
            assert ctx is not None
            original_ffmpeg = sticker_service.Ffmpeg
            sticker_service.Ffmpeg = FakeFfmpeg  # type: ignore[assignment]
            try:
                await sticker_service.create_sticker(ctx)
            finally:
                sticker_service.Ffmpeg = original_ffmpeg

            self.assertTrue(any(call[0] == "download_media" for call in bridge.calls))
            self.assertTrue(any(call[0] == "send_file_message" for call in bridge.calls))


if __name__ == "__main__":
    unittest.main()
