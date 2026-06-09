from __future__ import annotations

from pathlib import Path

from takeshi_bot import config
from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext
from takeshi_bot.errors import DangerError, WarningError
from takeshi_bot.paths import PROJECT_ROOT
from takeshi_bot.utils import random_name, remove_file_if_exists


def _context_text() -> str:
    parts = []
    for name in ("AGENTS.md", "README.md", "package.json"):
        path = PROJECT_ROOT / name
        if path.exists():
            parts.append(path.read_text(encoding="utf-8", errors="replace")[:12000])
    return "\n\n".join(parts)


async def handle(ctx: CommandContext) -> None:
    if not config.OPENAI_API_KEY:
        raise WarningError("O suporte inteligente nao esta disponivel no momento.")
    if ctx.is_video:
        raise WarningError("Nao consigo interpretar videos ainda! Envie imagem ou texto.")
    if ctx.is_audio:
        raise WarningError("Nao consigo interpretar audios ainda! Envie imagem ou texto.")

    text = ctx.full_args.strip() or ctx.reply_text
    if not text and not ctx.is_image:
        await ctx.send_reply(
            "*Takeshi Suporte*\n\nFaca sua pergunta sobre mim que eu te ajudarei!"
        )
        return
    if text and (len(text) < 5 or len(text) > 4096):
        raise DangerError("O texto deve ter entre 5 e 4096 caracteres.")

    await ctx.send_wait_reply("Analisando sua pergunta...")
    image_path = await ctx.download_image(random_name("support")) if ctx.is_image else None
    try:
        from openai import AsyncOpenAI

        client = AsyncOpenAI(api_key=config.OPENAI_API_KEY)
        user_content: list[dict[str, object]] = []
        if text:
            user_content.append({"type": "text", "text": text})
        if image_path:
            import base64

            encoded = base64.b64encode(Path(image_path).read_bytes()).decode("ascii")
            user_content.append(
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{encoded}", "detail": "low"},
                }
            )
        if not user_content:
            user_content.append({"type": "text", "text": "O que voce ve nesta imagem?"})
        response = await client.chat.completions.create(
            model="gpt-5-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Voce e um assistente especializado em suporte tecnico do Takeshi Bot. "
                        "Responda em portugues do Brasil, direto e com foco pratico."
                    ),
                },
                {"role": "system", "content": _context_text()},
                {"role": "user", "content": user_content},
            ],
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
