from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext

async def handle(ctx: CommandContext) -> None:
    await ctx.send_contact("+55 00 00000-0000", "Takeshi Bot")

command = Command("enviar-contato", "Exemplo de envio de contato.", ["enviar-contato"], "/enviar-contato", handle)
