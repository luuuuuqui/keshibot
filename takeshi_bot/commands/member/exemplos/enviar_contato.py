from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext

async def handle(ctx: CommandContext) -> None:
    await ctx.bridge.send_message(
        ctx.remote_jid,
        {
            "contacts": {
                "displayName": "Takeshi Bot",
                "contacts": [
                    {
                        "vcard": "BEGIN:VCARD\nVERSION:3.0\nFN:Takeshi Bot\nTEL;type=CELL;type=VOICE;waid=5500000000000:+55 00 00000-0000\nEND:VCARD"
                    }
                ],
            }
        },
    )

command = Command("enviar-contato", "Exemplo de envio de contato.", ["enviar-contato"], "/enviar-contato", handle)
