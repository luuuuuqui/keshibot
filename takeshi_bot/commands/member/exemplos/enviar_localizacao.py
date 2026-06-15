from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext

async def handle(ctx: CommandContext) -> None:
    await ctx.send_location(-23.55052, -46.633308)

command = Command("enviar-localizacao", "Exemplo de envio de localizacao.", ["enviar-localizacao"], "/enviar-localizacao", handle)
