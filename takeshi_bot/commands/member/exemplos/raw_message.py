from takeshi_bot.commands import Command
from ._helpers import raw_message_handle
command = Command("raw-message", "Exibe a mensagem bruta recebida.", ["raw-message"], "/raw-message", raw_message_handle)
