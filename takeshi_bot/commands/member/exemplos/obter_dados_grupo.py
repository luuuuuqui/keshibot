from takeshi_bot.commands import Command
from ._helpers import group_data_handle
command = Command("obter-dados-grupo", "Exemplo de dados do grupo.", ["obter-dados-grupo"], "/obter-dados-grupo", group_data_handle)
