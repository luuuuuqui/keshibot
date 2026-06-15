from __future__ import annotations

import json
from collections.abc import Awaitable, Callable
from typing import Any

from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext
from takeshi_bot.paths import ASSETS_DIR
from takeshi_bot.utils import as_dict, as_list

SAMPLES_DIR = ASSETS_DIR / "samples"
SAMPLE_IMAGE_URL = "https://api.spiderx.com.br/storage/samples/sample-image.jpg"
SPIDER_LOGO_URL = "https://api.spiderx.com.br/assets/images/logo.png"
ExampleHandler = Callable[[CommandContext], Awaitable[Any]]

EXAMPLE_ALIASES = {
    "enviar-botoes": ["enviar-botoes", "enviar-botao", "botoes-exemplo"],
    "enviar-codigo": ["enviar-codigo", "codigo"],
    "enviar-enquete": ["enviar-enquete", "poll-example", "exemplo-poll"],
    "enviar-latex": ["enviar-latex", "latex", "formula"],
    "enviar-lista": ["enviar-lista", "lista-exemplo", "enviar-list"],
    "enviar-reels": ["enviar-reels", "reels", "rich-reels"],
    "enviar-tabela": ["enviar-tabela", "tabela"],
    "enviar-texto-colorido": ["enviar-texto-colorido", "texto-colorido", "rich-texto"],
    "exemplo-gatilho": ["exemplo-gatilho", "gatilho-exemplo"],
    "exemplos-de-mensagens": [
        "exemplos-de-mensagens",
        "exemplos",
        "help-exemplos",
        "exemplo-de-mensagem",
        "exemplo-de-mensagens",
        "enviar-exemplos",
        "enviar-exemplo",
    ],
}


def _sample(name: str) -> str:
    return str(SAMPLES_DIR / name)


async def _send_document(ctx: CommandContext, file_path: str, file_name: str) -> None:
    await ctx.send_document_from_file(file_path, "application/pdf", file_name)


async def _send_poll(ctx: CommandContext) -> None:
    await ctx.send_poll(
        "Qual exemplo voce quer ver?",
        ["Texto", "Imagem", "Sticker"],
        single_choice=True,
    )


async def _send_buttons(ctx: CommandContext) -> None:
    trigger = _trigger_command(ctx, "opcao1")
    await ctx.bridge.send_message(
        ctx.remote_jid,
        {
            "text": "Exemplo de botoes no port Python.",
            "footer": "Takeshi Bot",
            "buttons": [
                {"buttonId": trigger, "buttonText": {"displayText": "Opcao 1"}},
                {
                    "buttonId": _trigger_command(ctx, "opcao2"),
                    "buttonText": {"displayText": "Opcao 2"},
                },
            ],
            "viewOnce": True,
        },
    )
    await ctx.bridge.send_message(
        ctx.remote_jid,
        {
            "text": "Exemplo com botoes interativos.",
            "footer": "Takeshi Bot",
            "interactiveButtons": [
                {
                    "name": "quick_reply",
                    "buttonParamsJson": json.dumps(
                        {
                            "display_text": "Interativo 1",
                            "id": _trigger_command(ctx, "interativo1"),
                        },
                        ensure_ascii=False,
                    ),
                },
                {
                    "name": "quick_reply",
                    "buttonParamsJson": json.dumps(
                        {
                            "display_text": "Interativo 2",
                            "id": _trigger_command(ctx, "interativo2"),
                        },
                        ensure_ascii=False,
                    ),
                },
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
                            "rowId": _trigger_command(ctx, "texto"),
                        },
                        {
                            "title": "Imagem",
                            "description": "Exemplo de imagem",
                            "rowId": _trigger_command(ctx, "imagem"),
                        },
                        {
                            "title": "Video",
                            "description": "Exemplo de video",
                            "rowId": _trigger_command(ctx, "video"),
                        },
                    ],
                },
                {
                    "title": "Interacao",
                    "rows": [
                        {
                            "title": "Botoes",
                            "description": "Exemplos com botoes",
                            "rowId": _trigger_command(ctx, "botoes"),
                        },
                        {
                            "title": "Carrossel",
                            "description": "Exemplos em formato de cards",
                            "rowId": _trigger_command(ctx, "carrossel"),
                        },
                    ],
                },
            ],
            "viewOnce": True,
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
                    "title": "Card 1: Imagem de exemplo",
                    "image": {"url": SAMPLE_IMAGE_URL},
                    "caption": "Primeira imagem do carrossel",
                },
                {
                    "title": "Card 2: Outra imagem",
                    "image": {"url": SPIDER_LOGO_URL},
                    "caption": "Segunda imagem com descricao diferente",
                },
                {
                    "title": "Card 3: Terceira opcao",
                    "image": {"url": SAMPLE_IMAGE_URL},
                    "caption": "Outro exemplo de card no carrossel",
                },
            ],
            "viewOnce": True,
        },
    )


def _trigger_command(ctx: CommandContext, parameter: str) -> str:
    return f"{ctx.prefix}exemplo-gatilho {parameter}"


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
        await ctx.send_edited_text("Mensagem editada do exemplo.", message)
    except Exception:
        await ctx.send_reply("Seu cliente/bridge nao aceitou edicao neste contexto.")


async def _send_trigger_example(ctx: CommandContext) -> None:
    await ctx.send_reply("Exemplo de gatilho executado com sucesso.")


async def _send_message_examples(ctx: CommandContext) -> None:
    await ctx.send_reply(
        "Exemplos disponiveis: texto, imagem, audio, video, sticker, documento, contato, localizacao."
    )


EXAMPLE_HANDLERS: dict[str, ExampleHandler] = {
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
    "enviar-documento-de-url": lambda ctx: ctx.send_document_from_url(
        "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
        "application/pdf",
        "dummy.pdf",
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
        commands=EXAMPLE_ALIASES.get(name, [name]),
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
    participants = [as_dict(item) for item in as_list(metadata.get("participants"))]
    await ctx.send_reply(
        "Dados do grupo\n\n"
        f"subject: {metadata.get('subject', '')}\n"
        f"id: {ctx.remote_jid}\n"
        f"participantes: {len(participants)}"
    )
