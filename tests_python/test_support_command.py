from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from typing import Any
from unittest.mock import patch

import takeshi_bot.commands.member.suporte as suporte


class FakeCompletions:
    def __init__(self, owner: "FakeOpenAI") -> None:
        self.owner = owner

    async def create(self, **kwargs: Any) -> Any:
        self.owner.calls.append(kwargs)
        message = type("Message", (), {"content": "Resposta do suporte"})()
        choice = type("Choice", (), {"message": message})()
        return type("Response", (), {"choices": [choice]})()


class FakeOpenAI:
    instances: list["FakeOpenAI"] = []

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.calls: list[dict[str, Any]] = []
        self.chat = type(
            "Chat",
            (),
            {"completions": FakeCompletions(self)},
        )()
        self.instances.append(self)


class FakeContext:
    def __init__(
        self,
        *,
        full_args: str = "",
        args: list[str] | None = None,
        reply_text: str = "",
        image_path: str | None = None,
    ) -> None:
        self.args = args or []
        self.full_args = full_args
        self.reply_text = reply_text
        self.is_image = image_path is not None
        self.is_video = False
        self.is_audio = False
        self.image_path = image_path
        self.calls: list[tuple[str, Any]] = []

    async def send_react(self, emoji: str) -> None:
        self.calls.append(("send_react", emoji))

    async def send_reply(self, text: str) -> None:
        self.calls.append(("send_reply", text))

    async def send_wait_reply(self, text: str) -> None:
        self.calls.append(("send_wait_reply", text))

    async def download_image(self, file_name: str) -> str | None:
        self.calls.append(("download_image", file_name))
        return self.image_path


class SupportCommandTest(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        FakeOpenAI.instances = []

    async def test_combines_reply_context_with_new_question(self) -> None:
        ctx = FakeContext(
            full_args="como resolver?",
            args=["como", "resolver?"],
            reply_text="erro 401 na Spider X",
        )

        with (
            patch.object(suporte.config, "OPENAI_API_KEY", "test-key"),
            patch.object(suporte, "AsyncOpenAI", FakeOpenAI),
        ):
            await suporte.handle(ctx)  # type: ignore[arg-type]

        messages = FakeOpenAI.instances[0].calls[0]["messages"]
        user_text = messages[-1]["content"][0]["text"]
        self.assertEqual(
            user_text,
            "Contexto anterior: erro 401 na Spider X\n\nNova questao: como resolver?",
        )
        self.assertIn(("send_reply", "Resposta do suporte"), ctx.calls)

    async def test_image_without_text_adds_default_visual_question(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            image = Path(tmp) / "erro.webp"
            image.write_bytes(b"WEBP")
            ctx = FakeContext(image_path=str(image))

            with (
                patch.object(suporte.config, "OPENAI_API_KEY", "test-key"),
                patch.object(suporte, "AsyncOpenAI", FakeOpenAI),
            ):
                await suporte.handle(ctx)  # type: ignore[arg-type]

        messages = FakeOpenAI.instances[0].calls[0]["messages"]
        user_content = messages[-1]["content"]
        self.assertEqual(user_content[0]["text"], "O que voce ve nesta imagem?")
        self.assertTrue(user_content[1]["image_url"]["url"].startswith("data:image/webp;base64,"))

    async def test_empty_prompt_shows_usage_without_openai_call(self) -> None:
        ctx = FakeContext()

        with (
            patch.object(suporte.config, "OPENAI_API_KEY", "test-key"),
            patch.object(suporte, "AsyncOpenAI", FakeOpenAI),
        ):
            await suporte.handle(ctx)  # type: ignore[arg-type]

        self.assertEqual(FakeOpenAI.instances, [])
        replies = [call[1] for call in ctx.calls if call[0] == "send_reply"]
        self.assertTrue(any("Takeshi Suporte" in reply for reply in replies))


if __name__ == "__main__":
    unittest.main()
