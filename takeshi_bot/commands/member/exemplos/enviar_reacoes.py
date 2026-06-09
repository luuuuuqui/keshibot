from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext

async def handle(ctx: CommandContext) -> None:
    await ctx.send_react("\u2705")
    await ctx.send_reply("Reacao enviada.")

command = Command("enviar-reacoes", "Exemplo de envio de reacoes.", ["enviar-reacoes"], "/enviar-reacoes", handle)
