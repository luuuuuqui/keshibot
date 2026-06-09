from __future__ import annotations

from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext
from takeshi_bot.errors import InvalidParameterError
from takeshi_bot.utils import only_numbers


async def handle(ctx: CommandContext) -> None:
    if len(ctx.args) != 3:
        raise InvalidParameterError("Uso: /fake-chat @usuario / texto citado / resposta")
    mentioned_lid = f"{only_numbers(ctx.args[0])}@lid"
    quoted_text = ctx.args[1]
    response_text = ctx.args[2]
    if len(quoted_text) < 2:
        raise InvalidParameterError("O texto citado deve ter pelo menos 2 caracteres.")
    if len(response_text) < 2:
        raise InvalidParameterError("A mensagem de resposta deve ter pelo menos 2 caracteres.")
    fake_quoted = {
        "key": {
            "fromMe": False,
            "participant": mentioned_lid,
            "remoteJid": ctx.remote_jid,
        },
        "message": {
            "extendedTextMessage": {
                "text": quoted_text,
                "contextInfo": {"mentionedJid": [mentioned_lid]},
            }
        },
    }
    await ctx.bridge.send_message(
        ctx.remote_jid,
        {"text": response_text},
        {"quoted": fake_quoted},
    )


command = Command(
    name="fake-chat",
    description="Cria uma citacao falsa mencionando usuario.",
    commands=["fake-chat", "fq", "fake-quote", "f-quote", "fk"],
    usage="/fake-chat @usuario / texto citado / resposta",
    handle=handle,
)
