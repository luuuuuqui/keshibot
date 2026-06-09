from __future__ import annotations

from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext
from takeshi_bot.errors import InvalidParameterError


async def handle(ctx: CommandContext) -> None:
    context_info = (
        ctx.web_message.get("message", {})
        .get("extendedTextMessage", {})
        .get("contextInfo", {})
    )
    stanza_id = context_info.get("stanzaId")
    participant = context_info.get("participant")
    if not stanza_id or not participant:
        raise InvalidParameterError("Voce deve mencionar uma mensagem para excluir!")
    await ctx.delete_message(
        {
            "remoteJid": ctx.remote_jid,
            "fromMe": False,
            "id": stanza_id,
            "participant": participant,
        }
    )


command = Command(
    name="delete",
    description="Exclui mensagens mencionadas.",
    commands=["delete", "d"],
    usage="/delete",
    handle=handle,
)
