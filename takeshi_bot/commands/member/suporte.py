from __future__ import annotations

import base64
from pathlib import Path
from typing import Any

try:
    from openai import AsyncOpenAI
except ModuleNotFoundError:  # pragma: no cover - exercised by handle when needed.
    AsyncOpenAI = None  # type: ignore[assignment]

from takeshi_bot import config
from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext
from takeshi_bot.errors import DangerError, WarningError
from takeshi_bot.paths import PROJECT_ROOT
from takeshi_bot.utils import random_name, remove_file_if_exists


def _context_text() -> str:
    parts: list[str] = []
    for name in ("AGENTS.md", "README.md", "package.json"):
        path = PROJECT_ROOT / name
        if path.exists():
            parts.append(path.read_text(encoding="utf-8", errors="replace")[:12000])
    return "\n\n".join(parts)


def _support_text(ctx: CommandContext) -> str:
    has_args = bool(ctx.args)
    text = ctx.full_args.strip() if has_args else ctx.reply_text.strip()
    if has_args and ctx.reply_text:
        return f"Contexto anterior: {ctx.reply_text}\n\nNova questao: {text}"
    return text


def _image_mime_type(image_path: str) -> str:
    extension = Path(image_path).suffix.lower()
    return {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
        ".gif": "image/gif",
    }.get(extension, "image/jpeg")


def _image_content_part(image_path: str) -> dict[str, Any]:
    encoded = base64.b64encode(Path(image_path).read_bytes()).decode("ascii")
    return {
        "type": "image_url",
        "image_url": {
            "url": f"data:{_image_mime_type(image_path)};base64,{encoded}",
            "detail": "low",
        },
    }


async def handle(ctx: CommandContext) -> None:
    if not config.OPENAI_API_KEY:
        raise WarningError("O suporte inteligente nao esta disponivel no momento.")
    if ctx.is_video:
        raise WarningError("Nao consigo interpretar videos ainda! Envie imagem ou texto.")
    if ctx.is_audio:
        raise WarningError("Nao consigo interpretar audios ainda! Envie imagem ou texto.")

    text = _support_text(ctx)
    if not text and not ctx.is_image:
        await ctx.send_react(config.BOT_EMOJI)
        await ctx.send_reply(
            "*Takeshi Suporte*\n\n"
            "Faca sua pergunta sobre mim que eu te ajudarei!\n\n"
            "- /suporte bot desliga sozinho\n"
            "- /suporte como instalar no Termux?\n"
            "- /suporte erro 401 API Spider X\n"
            "- Envie uma imagem com /suporte para analise visual"
        )
        return
    if text and len(text) < 5:
        raise DangerError("O texto deve ter no minimo 5 caracteres.")
    if text and len(text) > 4096:
        raise DangerError("O texto deve ter no maximo 4096 caracteres.")

    await ctx.send_wait_reply("Analisando sua pergunta...")
    image_path = await ctx.download_image(random_name("support")) if ctx.is_image else None
    try:
        if AsyncOpenAI is None:
            raise WarningError("A dependencia openai nao esta instalada no ambiente.")
        client = AsyncOpenAI(api_key=config.OPENAI_API_KEY)
        user_content: list[dict[str, Any]] = []
        if text:
            user_content.append({"type": "text", "text": text})
        if image_path:
            if not text:
                user_content.append({"type": "text", "text": "O que voce ve nesta imagem?"})
            user_content.append(_image_content_part(image_path))
        if not user_content:
            user_content.append({"type": "text", "text": "O que voce ve nesta imagem?"})
        messages: list[dict[str, Any]] = [
            {
                "role": "system",
                "content": (
                    "Voce e um assistente especializado em suporte tecnico do Takeshi Bot. "
                    "Responda em portugues do Brasil, direto e com foco pratico."
                ),
            },
            {"role": "system", "content": _context_text()},
            {"role": "user", "content": user_content},
        ]
        response = await client.chat.completions.create(
            model="gpt-5-mini",
            messages=messages,
            max_completion_tokens=2048,
        )
        answer = (response.choices[0].message.content or "").strip()
        if not answer:
            raise DangerError("Nao consegui encontrar uma resposta para sua pergunta.")
        await ctx.send_react(config.BOT_EMOJI)
        await ctx.send_reply(answer)
    finally:
        remove_file_if_exists(image_path)


command = Command(
    name="suporte",
    description="Suporte inteligente do Takeshi usando IA.",
    commands=["suporte", "help", "ajuda"],
    usage="/suporte como instalar o Takeshi?",
    handle=handle,
)
