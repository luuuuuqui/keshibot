from __future__ import annotations

import json
from pathlib import Path

from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext
from takeshi_bot.paths import ASSETS_DIR

SAMPLES_DIR = ASSETS_DIR / "samples"


def _sample(name: str) -> str:
    return str(SAMPLES_DIR / name)


async def _send_document(ctx: CommandContext, file_path: str, file_name: str) -> None:
    await ctx.bridge.send_file_message(
        ctx.remote_jid,
        "document",
        file_path,
        {"mimetype": "application/pdf", "fileName": file_name},
        ctx._quoted_option(True),
    )


async def _send_poll(ctx: CommandContext) -> None:
    await ctx.bridge.send_message(
        ctx.remote_jid,
        {
            "poll": {
                "name": "Qual exemplo voce quer ver?",
                "values": ["Texto", "Imagem", "Sticker"],
                "selectableCount": 1,
            }
        },
    )


async def _send_buttons(ctx: CommandContext) -> None:
    await ctx.bridge.send_message(
        ctx.remote_jid,
        {
            "text": "Exemplo de botoes no port Python.",
            "footer": "Takeshi Bot",
            "buttons": [
                {"buttonId": "exemplo_ok", "buttonText": {"displayText": "OK"}},
                {"buttonId": "exemplo_menu", "buttonText": {"displayText": "Menu"}},
            ],
            "viewOnce": True,
        },
    )


async def _send_list(ctx: CommandContext) -> None:
    await ctx.bridge.send_message(
        ctx.remote_jid,
        {
            "text": "Exemplo de lista no port Python.",
            "footer": "Takeshi Bot",
            "title": "Exemplos",
            "buttonText": "Abrir lista",
            "sections": [
                {
                    "title": "Envios",
                    "rows": [
                        {
                            "title": "Texto",
                            "description": "Exemplo de texto",
                            "rowId": "enviar-texto",
                        },
                        {
                            "title": "Imagem",
                            "description": "Exemplo de imagem",
                            "rowId": "enviar-imagem-de-arquivo",
                        },
                    ],
                }
            ],
        },
    )


async def _send_carousel(ctx: CommandContext) -> None:
    await ctx.bridge.send_message(
        ctx.remote_jid,
        {
            "text": "Exemplo de carrossel no port Python.",
            "footer": "Takeshi Bot",
            "cards": [
                {
                    "title": "Imagem local",
                    "image": {"url": _sample("sample-image.jpg")},
                    "caption": "Card de exemplo",
                }
            ],
            "viewOnce": True,
        },
    )


async def _send_code(ctx: CommandContext) -> None:
    await ctx.send_reply("```python\nawait ctx.send_reply('Ola do Python')\n```")


async def _send_table(ctx: CommandContext) -> None:
    await ctx.send_reply(
        "```text\n"
        "+----------+---------+\n"
        "| Recurso  | Status  |\n"
        "+----------+---------+\n"
        "| Python   | OK      |\n"
        "| Bridge   | OK      |\n"
        "+----------+---------+\n"
        "```"
    )


async def _send_latex(ctx: CommandContext) -> None:
    await ctx.send_reply("Exemplo LaTeX: `E = mc^2`")


async def _send_colored_text(ctx: CommandContext) -> None:
    await ctx.send_reply("Exemplo de texto colorido: recurso dependente do cliente WhatsApp.")


async def _send_reels(ctx: CommandContext) -> None:
    await ctx.send_video_from_file(_sample("sample-video.mp4"), "Exemplo de reels/video.")


async def _send_edited_message(ctx: CommandContext) -> None:
    message = await ctx.send_text("Mensagem original do exemplo.")
    try:
        await ctx.bridge.send_message(
            ctx.remote_jid,
            {"text": "Mensagem editada do exemplo.", "edit": message.get("key")},
        )
    except Exception:
        await ctx.send_reply("Seu cliente/bridge nao aceitou edicao neste contexto.")


async def _send_trigger_example(ctx: CommandContext) -> None:
    await ctx.send_reply("Exemplo de gatilho executado com sucesso.")


async def _send_message_examples(ctx: CommandContext) -> None:
    await ctx.send_reply(
        "Exemplos disponiveis: texto, imagem, audio, video, sticker, documento, contato, localizacao."
    )


EXAMPLE_HANDLERS = {
    "enviar-audio-de-arquivo": lambda ctx: ctx.send_audio_from_file(
        _sample("sample-audio.mp3")
    ),
    "enviar-audio-de-buffer": lambda ctx: ctx.send_audio_from_file(
        _sample("sample-audio.mp3")
    ),
    "enviar-audio-de-url": lambda ctx: ctx.send_audio_from_url(
        "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
    ),
    "enviar-botoes": _send_buttons,
    "enviar-carrossel": _send_carousel,
    "enviar-codigo": _send_code,
    "enviar-documento-de-arquivo": lambda ctx: _send_document(
        ctx, _sample("sample-document.pdf"), "sample-document.pdf"
    ),
    "enviar-documento-de-buffer": lambda ctx: _send_document(
        ctx, _sample("sample-document.pdf"), "sample-document.pdf"
    ),
    "enviar-documento-de-url": lambda ctx: ctx.bridge.send_message(
        ctx.remote_jid,
        {
            "document": {"url": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"},
            "mimetype": "application/pdf",
            "fileName": "dummy.pdf",
        },
        ctx._quoted_option(True),
    ),
    "enviar-enquete": _send_poll,
    "enviar-gif-de-arquivo": lambda ctx: ctx.send_gif_from_file(
        _sample("sample-video.mp4"), "Exemplo de GIF local."
    ),
    "enviar-gif-de-buffer": lambda ctx: ctx.send_gif_from_file(
        _sample("sample-video.mp4"), "Exemplo de GIF por buffer."
    ),
    "enviar-gif-de-url": lambda ctx: ctx.send_gif_from_url(
        "https://media.giphy.com/media/ICOgUNjpvO0PC/giphy.gif",
        "Exemplo de GIF por URL.",
    ),
    "enviar-imagem-de-arquivo": lambda ctx: ctx.send_image_from_file(
        _sample("sample-image.jpg"), "Exemplo de imagem local."
    ),
    "enviar-imagem-de-buffer": lambda ctx: ctx.send_image_from_file(
        _sample("sample-image.jpg"), "Exemplo de imagem por buffer."
    ),
    "enviar-imagem-de-url": lambda ctx: ctx.send_image_from_url(
        "https://picsum.photos/800/600", "Exemplo de imagem por URL."
    ),
    "enviar-latex": _send_latex,
    "enviar-lista": _send_list,
    "enviar-mensagem-editada": _send_edited_message,
    "enviar-reels": _send_reels,
    "enviar-sticker-de-arquivo": lambda ctx: ctx.send_sticker_from_file(
        _sample("sample-sticker.webp")
    ),
    "enviar-sticker-de-buffer": lambda ctx: ctx.send_sticker_from_file(
        _sample("sample-sticker.webp")
    ),
    "enviar-sticker-de-url": lambda ctx: ctx.send_sticker_from_url(
        "https://www.gstatic.com/webp/gallery/1.webp"
    ),
    "enviar-tabela": _send_table,
    "enviar-texto-colorido": _send_colored_text,
    "enviar-video-de-arquivo": lambda ctx: ctx.send_video_from_file(
        _sample("sample-video.mp4"), "Exemplo de video local."
    ),
    "enviar-video-de-buffer": lambda ctx: ctx.send_video_from_file(
        _sample("sample-video.mp4"), "Exemplo de video por buffer."
    ),
    "enviar-video-de-url": lambda ctx: ctx.send_video_from_url(
        "https://samplelib.com/lib/preview/mp4/sample-5s.mp4",
        "Exemplo de video por URL.",
    ),
    "exemplo-gatilho": _send_trigger_example,
    "exemplos-de-mensagens": _send_message_examples,
}


def make_example_command(name: str, description: str | None = None) -> Command:
    async def handle(ctx: CommandContext) -> None:
        specific_handler = EXAMPLE_HANDLERS.get(name)
        if specific_handler:
            await specific_handler(ctx)
            return

        await ctx.send_reply(
            f"Exemplo Python: {name}\n\n"
            "Este comando existe para manter paridade estrutural com os exemplos JS. "
            "Use os helpers do CommandContext para montar uma demonstracao mais especifica."
        )

    return Command(
        name=name,
        description=description or f"Exemplo Python para {name}.",
        commands=[name],
        usage=f"/{name}",
        handle=handle,
    )


async def raw_message_handle(ctx: CommandContext) -> None:
    payload = json.dumps(ctx.web_message, ensure_ascii=False, indent=2)[:3500]
    await ctx.send_reply(f"```json\n{payload}\n```")


async def metadata_handle(ctx: CommandContext) -> None:
    await ctx.send_reply(
        "Metadados da mensagem\n\n"
        f"remote_jid: {ctx.remote_jid}\n"
        f"user_lid: {ctx.user_lid}\n"
        f"command: {ctx.command_name}\n"
        f"args: {ctx.args}\n"
        f"is_reply: {ctx.is_reply}\n"
        f"is_image: {ctx.is_image}\n"
        f"is_video: {ctx.is_video}\n"
        f"is_audio: {ctx.is_audio}\n"
        f"is_sticker: {ctx.is_sticker}"
    )


async def group_data_handle(ctx: CommandContext) -> None:
    metadata = await ctx.bridge.group_metadata(ctx.remote_jid)
    participants = metadata.get("participants") or []
    await ctx.send_reply(
        "Dados do grupo\n\n"
        f"subject: {metadata.get('subject', '')}\n"
        f"id: {ctx.remote_jid}\n"
        f"participantes: {len(participants)}"
    )
