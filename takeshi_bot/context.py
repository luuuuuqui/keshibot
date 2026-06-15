from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Any

from . import config
from .bridge import BaileysBridge
from .utils import baileys_is, extract_data_from_message, only_numbers, random_name


@dataclass
class CommandContext:
    bridge: BaileysBridge
    web_message: dict[str, Any]
    args: list[str]
    command_name: str
    full_args: str
    full_message: str
    is_reply: bool
    prefix: str
    remote_jid: str
    reply_lid: str | None
    reply_text: str
    user_lid: str
    is_audio: bool
    is_group: bool
    is_group_with_lid: bool
    is_image: bool
    is_sticker: bool
    is_video: bool
    type: str = ""
    start_process: float | None = None

    @classmethod
    def from_web_message(
        cls,
        bridge: BaileysBridge,
        web_message: dict[str, Any],
        start_process: float | None = None,
    ) -> "CommandContext | None":
        data = extract_data_from_message(web_message)
        remote_jid = data.get("remote_jid")
        if not remote_jid:
            return None
        return cls(
            bridge=bridge,
            web_message=web_message,
            args=data["args"],
            command_name=data["command_name"],
            full_args=data["full_args"],
            full_message=data["full_message"],
            is_reply=data["is_reply"],
            prefix=data["prefix"],
            remote_jid=remote_jid,
            reply_lid=data["reply_lid"],
            reply_text=data["reply_text"],
            user_lid=data["user_lid"],
            is_audio=baileys_is(web_message, "audio"),
            is_group=remote_jid.endswith("@g.us"),
            is_group_with_lid=remote_jid.endswith("@g.us") and bool(data["user_lid"]),
            is_image=baileys_is(web_message, "image"),
            is_sticker=baileys_is(web_message, "sticker"),
            is_video=baileys_is(web_message, "video"),
            start_process=start_process,
        )

    async def send_typing_state(self, another_jid: str = "") -> None:
        await self.bridge.send_presence(another_jid or self.remote_jid, "composing")
        await asyncio.sleep(config.TIMEOUT_IN_MILLISECONDS_BY_EVENT / 1000)

    async def send_record_state(self, another_jid: str = "") -> None:
        await self.bridge.send_presence(another_jid or self.remote_jid, "recording")
        await asyncio.sleep(config.TIMEOUT_IN_MILLISECONDS_BY_EVENT / 1000)

    def _quoted_option(self, quoted: bool = True) -> dict[str, Any]:
        return {"quoted": self.web_message} if quoted else {}

    def quoted_option(self, quoted: bool = True) -> dict[str, Any]:
        return self._quoted_option(quoted)

    async def send_text(self, text: str, mentions: list[str] | None = None) -> Any:
        await self.send_typing_state()
        content: dict[str, Any] = {"text": f"{config.BOT_EMOJI} {text}"}
        if mentions:
            content["mentions"] = mentions
        return await self.bridge.send_message(self.remote_jid, content)

    async def send_reply(self, text: str, mentions: list[str] | None = None) -> Any:
        await self.send_typing_state()
        content: dict[str, Any] = {"text": f"{config.BOT_EMOJI} {text}"}
        if mentions:
            content["mentions"] = mentions
        return await self.bridge.send_message(
            self.remote_jid, content, self._quoted_option(True)
        )

    async def send_edited_text(
        self,
        text: str,
        message_to_edit: dict[str, Any],
        mentions: list[str] | None = None,
    ) -> Any:
        content: dict[str, Any] = {
            "text": f"{config.BOT_EMOJI} {text}",
            "edit": message_to_edit.get("key"),
        }
        if mentions:
            content["mentions"] = mentions
        return await self.bridge.send_message(self.remote_jid, content)

    async def send_edited_reply(
        self,
        text: str,
        message_to_edit: dict[str, Any],
        mentions: list[str] | None = None,
    ) -> Any:
        content: dict[str, Any] = {
            "text": f"{config.BOT_EMOJI} {text}",
            "edit": message_to_edit.get("key"),
        }
        if mentions:
            content["mentions"] = mentions
        return await self.bridge.send_message(
            self.remote_jid, content, self._quoted_option(True)
        )

    async def send_react(self, emoji: str, msg_key: dict[str, Any] | None = None) -> Any:
        return await self.bridge.send_message(
            self.remote_jid,
            {"react": {"text": emoji, "key": msg_key or self.web_message.get("key")}},
        )

    async def send_success_reply(self, text: str) -> Any:
        await self.send_react("\u2705")
        return await self.send_reply(f"\u2705 {text}")

    async def send_wait_reply(self, text: str = "Carregando dados...") -> Any:
        await self.send_react("\u23f3")
        return await self.send_reply(f"\u23f3 Aguarde! {text}")

    async def send_warning_reply(self, text: str) -> Any:
        await self.send_react("\u26a0\ufe0f")
        return await self.send_reply(f"\u26a0\ufe0f Atencao! {text}")

    async def send_error_reply(self, text: str) -> Any:
        await self.send_react("\u274c")
        return await self.send_reply(f"\u274c Erro! {text}")

    async def delete_message(self, key: dict[str, Any]) -> Any:
        return await self.bridge.delete_message(self.remote_jid, key)

    async def download_audio(self, file_name: str | None = None) -> str | None:
        return await self.bridge.download_media(
            self.web_message, "audio", file_name or random_name("audio"), "mpeg"
        )

    async def download_image(self, file_name: str | None = None) -> str | None:
        return await self.bridge.download_media(
            self.web_message, "image", file_name or random_name("image"), "png"
        )

    async def download_sticker(self, file_name: str | None = None) -> str | None:
        return await self.bridge.download_media(
            self.web_message, "sticker", file_name or random_name("sticker"), "webp"
        )

    async def download_video(self, file_name: str | None = None) -> str | None:
        return await self.bridge.download_media(
            self.web_message, "video", file_name or random_name("video"), "mp4"
        )

    async def send_image_from_url(
        self, url: str, caption: str = "", quoted: bool = True
    ) -> Any:
        content: dict[str, Any] = {"image": {"url": url}}
        if caption:
            content["caption"] = caption
        return await self.bridge.send_message(
            self.remote_jid, content, self._quoted_option(quoted)
        )

    async def send_video_from_url(
        self, url: str, caption: str = "", quoted: bool = True
    ) -> Any:
        content: dict[str, Any] = {"video": {"url": url}}
        if caption:
            content["caption"] = caption
        return await self.bridge.send_message(
            self.remote_jid, content, self._quoted_option(quoted)
        )

    async def send_gif_from_url(
        self, url: str, caption: str = "", quoted: bool = True
    ) -> Any:
        content: dict[str, Any] = {"video": {"url": url}, "gifPlayback": True}
        if caption:
            content["caption"] = caption
        return await self.bridge.send_message(
            self.remote_jid, content, self._quoted_option(quoted)
        )

    async def send_audio_from_url(
        self, url: str, as_voice: bool = False, quoted: bool = True
    ) -> Any:
        content: dict[str, Any] = {
            "audio": {"url": url},
            "mimetype": "audio/mpeg",
            "ptt": as_voice,
        }
        return await self.bridge.send_message(
            self.remote_jid, content, self._quoted_option(quoted)
        )

    async def send_sticker_from_url(self, url: str, quoted: bool = True) -> Any:
        return await self.bridge.send_message(
            self.remote_jid, {"sticker": {"url": url}}, self._quoted_option(quoted)
        )

    async def send_contact(self, phone_number: str, display_name: str) -> Any:
        phone_number_hydrated = only_numbers(phone_number)
        vcard = (
            "BEGIN:VCARD\n"
            "VERSION:3.0\n"
            f"FN:{display_name}\n"
            f"TEL;type=CELL;type=VOICE;waid={phone_number_hydrated}:{phone_number}\n"
            "END:VCARD"
        )
        return await self.bridge.send_message(
            self.remote_jid,
            {
                "contacts": {
                    "displayName": display_name,
                    "contacts": [{"vcard": vcard}],
                }
            },
        )

    async def send_location(self, latitude: float, longitude: float) -> Any:
        return await self.bridge.send_message(
            self.remote_jid,
            {
                "location": {
                    "degreesLatitude": latitude,
                    "degreesLongitude": longitude,
                }
            },
        )

    async def send_sticker_from_file(self, file_path: str, quoted: bool = True) -> Any:
        return await self.bridge.send_file_message(
            self.remote_jid, "sticker", file_path, {}, self._quoted_option(quoted)
        )

    async def send_document_from_url(
        self,
        url: str,
        mimetype: str = "application/octet-stream",
        file_name: str = "documento.pdf",
        quoted: bool = True,
    ) -> Any:
        return await self.bridge.send_message(
            self.remote_jid,
            {
                "document": {"url": url},
                "mimetype": mimetype,
                "fileName": file_name,
            },
            self._quoted_option(quoted),
        )

    async def send_document_from_file(
        self,
        file_path: str,
        mimetype: str = "application/octet-stream",
        file_name: str = "documento.pdf",
        quoted: bool = True,
    ) -> Any:
        return await self.bridge.send_file_message(
            self.remote_jid,
            "document",
            file_path,
            {"mimetype": mimetype, "fileName": file_name},
            self._quoted_option(quoted),
        )

    async def send_document_from_buffer(
        self,
        buffer: bytes,
        mimetype: str = "application/octet-stream",
        file_name: str = "documento.pdf",
        quoted: bool = True,
    ) -> Any:
        from pathlib import Path

        from takeshi_bot.paths import TEMP_DIR

        TEMP_DIR.mkdir(parents=True, exist_ok=True)
        file_path = TEMP_DIR / random_name("bin")
        Path(file_path).write_bytes(buffer)
        try:
            return await self.send_document_from_file(
                str(file_path), mimetype, file_name, quoted
            )
        finally:
            file_path.unlink(missing_ok=True)

    async def send_image_from_file(
        self, file_path: str, caption: str = "", quoted: bool = True
    ) -> Any:
        content: dict[str, Any] = {}
        if caption:
            content["caption"] = caption
        return await self.bridge.send_file_message(
            self.remote_jid, "image", file_path, content, self._quoted_option(quoted)
        )

    async def send_image_from_buffer(
        self, buffer: bytes, caption: str = "", quoted: bool = True
    ) -> Any:
        from pathlib import Path

        from takeshi_bot.paths import TEMP_DIR
        from takeshi_bot.utils import random_name

        file_path = TEMP_DIR / random_name("png")
        Path(file_path).write_bytes(buffer)
        try:
            return await self.send_image_from_file(str(file_path), caption, quoted)
        finally:
            file_path.unlink(missing_ok=True)

    async def send_audio_from_file(
        self, file_path: str, as_voice: bool = False, quoted: bool = True
    ) -> Any:
        content: dict[str, Any] = {"mimetype": "audio/mpeg", "ptt": as_voice}
        return await self.bridge.send_file_message(
            self.remote_jid, "audio", file_path, content, self._quoted_option(quoted)
        )

    async def send_video_from_file(
        self, file_path: str, caption: str = "", quoted: bool = True
    ) -> Any:
        content: dict[str, Any] = {}
        if caption:
            content["caption"] = caption
        return await self.bridge.send_file_message(
            self.remote_jid, "video", file_path, content, self._quoted_option(quoted)
        )

    async def send_gif_from_file(
        self,
        file_path: str,
        caption: str = "",
        mentions: list[str] | None = None,
        quoted: bool = True,
    ) -> Any:
        content: dict[str, Any] = {"gifPlayback": True}
        if caption:
            content["caption"] = caption
        if mentions:
            content["mentions"] = mentions
        return await self.bridge.send_file_message(
            self.remote_jid, "video", file_path, content, self._quoted_option(quoted)
        )
