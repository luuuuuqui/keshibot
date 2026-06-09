from takeshi_bot.commands import Command
from ._helpers import group_data_handle
command = Command("funcoes-grupo", "Exemplo de funcoes de grupo.", ["funcoes-grupo"], "/funcoes-grupo", group_data_handle)
