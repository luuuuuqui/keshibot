from takeshi_bot.commands import Command

from ._helpers import metadata_handle

command = Command(
    "obter-metadados-mensagem",
    "Exemplo de metadados da mensagem.",
    ["obter-metadados-mensagem", "metadados", "info-msg"],
    "/obter-metadados-mensagem",
    metadata_handle,
)
