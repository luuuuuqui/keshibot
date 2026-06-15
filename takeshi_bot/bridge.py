from __future__ import annotations

import asyncio
import json
import sys
import uuid
from collections.abc import AsyncIterator
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .paths import BRIDGE_SCRIPT


class BridgeError(RuntimeError):
    pass


@dataclass
class BridgeEvent:
    type: str
    payload: dict[str, Any]


class BaileysBridge:
    def __init__(
        self,
        script_path: Path = BRIDGE_SCRIPT,
        node_binary: str = "node",
    ) -> None:
        self.script_path = script_path
        self.node_binary = node_binary
        self.process: asyncio.subprocess.Process | None = None
        self._pending: dict[str, asyncio.Future[Any]] = {}
        self._events: asyncio.Queue[BridgeEvent] = asyncio.Queue()
        self._reader_task: asyncio.Task[None] | None = None
        self._stderr_task: asyncio.Task[None] | None = None

    async def start(self) -> None:
        if self.process is not None:
            return
        if not self.script_path.exists():
            raise BridgeError(f"Bridge script not found: {self.script_path}")
        self.process = await asyncio.create_subprocess_exec(
            self.node_binary,
            str(self.script_path),
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        self._reader_task = asyncio.create_task(self._read_stdout())
        self._stderr_task = asyncio.create_task(self._read_stderr())

    async def stop(self) -> None:
        if self.process is None:
            return
        if self.process.returncode is None:
            self.process.terminate()
            try:
                await asyncio.wait_for(self.process.wait(), timeout=5)
            except asyncio.TimeoutError:
                self.process.kill()
                await self.process.wait()
        for task in (self._reader_task, self._stderr_task):
            if task:
                task.cancel()
        self.process = None

    async def _read_stdout(self) -> None:
        assert self.process and self.process.stdout
        while True:
            line = await self.process.stdout.readline()
            if not line:
                break
            try:
                message = json.loads(line.decode("utf-8"))
            except json.JSONDecodeError:
                continue
            kind = message.get("kind")
            if kind == "response":
                future = self._pending.pop(message.get("id"), None)
                if future is None:
                    continue
                if message.get("ok"):
                    future.set_result(message.get("data"))
                else:
                    future.set_exception(BridgeError(message.get("error", "Bridge error")))
            elif kind == "event":
                await self._events.put(
                    BridgeEvent(
                        type=message.get("type", ""),
                        payload=message.get("payload") or {},
                    )
                )

    async def _read_stderr(self) -> None:
        assert self.process and self.process.stderr
        while True:
            line = await self.process.stderr.readline()
            if not line:
                break
            sys.stderr.write(line.decode("utf-8", errors="replace"))

    async def request(self, action: str, payload: dict[str, Any] | None = None) -> Any:
        if self.process is None or self.process.stdin is None:
            raise BridgeError("Bridge process is not running")
        request_id = str(uuid.uuid4())
        loop = asyncio.get_running_loop()
        future: asyncio.Future[Any] = loop.create_future()
        self._pending[request_id] = future
        body = {
            "id": request_id,
            "action": action,
            "payload": payload or {},
        }
        self.process.stdin.write((json.dumps(body, ensure_ascii=False) + "\n").encode())
        await self.process.stdin.drain()
        return await future

    async def events(self) -> AsyncIterator[BridgeEvent]:
        while True:
            yield await self._events.get()

    async def send_message(
        self,
        remote_jid: str,
        content: dict[str, Any],
        options: dict[str, Any] | None = None,
    ) -> Any:
        return await self.request(
            "send_message",
            {"remoteJid": remote_jid, "content": content, "options": options or {}},
        )

    async def send_file_message(
        self,
        remote_jid: str,
        media_key: str,
        file_path: str,
        content: dict[str, Any] | None = None,
        options: dict[str, Any] | None = None,
    ) -> Any:
        return await self.request(
            "send_file_message",
            {
                "remoteJid": remote_jid,
                "mediaKey": media_key,
                "filePath": file_path,
                "content": content or {},
                "options": options or {},
            },
        )

    async def send_presence(self, remote_jid: str, presence: str) -> Any:
        return await self.request(
            "send_presence", {"remoteJid": remote_jid, "presence": presence}
        )

    async def delete_message(self, remote_jid: str, key: dict[str, Any]) -> Any:
        return await self.request("delete_message", {"remoteJid": remote_jid, "key": key})

    async def group_participants_update(
        self, remote_jid: str, participants: list[str], operation: str
    ) -> Any:
        return await self.request(
            "group_participants_update",
            {
                "remoteJid": remote_jid,
                "participants": participants,
                "operation": operation,
            },
        )

    async def group_metadata(self, remote_jid: str) -> dict[str, Any]:
        return await self.request("group_metadata", {"remoteJid": remote_jid})

    async def group_setting_update(self, remote_jid: str, setting: str) -> Any:
        return await self.request(
            "group_setting_update", {"remoteJid": remote_jid, "setting": setting}
        )

    async def group_invite_code(self, remote_jid: str) -> str:
        return await self.request("group_invite_code", {"remoteJid": remote_jid})

    async def group_update_subject(self, remote_jid: str, subject: str) -> Any:
        return await self.request(
            "group_update_subject", {"remoteJid": remote_jid, "subject": subject}
        )

    async def update_profile_name(self, name: str) -> Any:
        return await self.request("update_profile_name", {"name": name})

    async def update_block_status(self, jid: str, status: str) -> Any:
        return await self.request(
            "update_block_status", {"jid": jid, "status": status}
        )

    async def profile_picture_url(self, jid: str, image_type: str = "image") -> str:
        return await self.request(
            "profile_picture_url", {"jid": jid, "type": image_type}
        )

    async def download_media(
        self, web_message: dict[str, Any], context: str, file_name: str, extension: str
    ) -> str | None:
        return await self.request(
            "download_media",
            {
                "webMessage": web_message,
                "context": context,
                "fileName": file_name,
                "extension": extension,
            },
        )

    async def add_sticker_metadata(
        self,
        input_path: str,
        output_path: str,
        metadata: dict[str, Any],
    ) -> str:
        return await self.request(
            "add_sticker_metadata",
            {
                "inputPath": input_path,
                "outputPath": output_path,
                "metadata": metadata,
            },
        )
