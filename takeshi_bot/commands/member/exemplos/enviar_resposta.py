from takeshi_bot.commands import Command
from takeshi_bot.context import CommandContext

async def handle(ctx: CommandContext) -> None:
    await ctx.send_reply("Esta e uma resposta citando sua mensagem.")

command = Command("enviar-resposta", "Exemplo de resposta citada.", ["enviar-resposta"], "/enviar-resposta", handle)
