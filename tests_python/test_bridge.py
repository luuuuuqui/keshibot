from __future__ import annotations

import unittest
from typing import Any

from takeshi_bot.bridge import BaileysBridge


class RecordingBridge(BaileysBridge):
    def __init__(self) -> None:
        super().__init__()
        self.calls: list[tuple[str, dict[str, Any]]] = []

    async def request(self, action: str, payload: dict[str, Any] | None = None) -> Any:
        self.calls.append((action, payload or {}))
        return "https://example.com/profile.jpg"


class BridgeTest(unittest.IsolatedAsyncioTestCase):
    async def test_profile_picture_url_uses_sidecar_action(self) -> None:
        bridge = RecordingBridge()

        result = await bridge.profile_picture_url("user@lid", "preview")

        self.assertEqual(result, "https://example.com/profile.jpg")
        self.assertEqual(
            bridge.calls,
            [("profile_picture_url", {"jid": "user@lid", "type": "preview"})],
        )


if __name__ == "__main__":
    unittest.main()
