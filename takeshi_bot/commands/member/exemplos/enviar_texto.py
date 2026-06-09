from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext

async def handle(ctx: CommandContext) -> None:
    await ctx.send_text("Exemplo de envio de texto.")

command = Command("enviar-texto", "Exemplo de envio de texto.", ["enviar-texto"], "/enviar-texto", handle)
