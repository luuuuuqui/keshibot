from takeshi_bot.commands import Command
from ._helpers import dice_handle

command = Command(
    name="dado",
    description="Joga um dado de 1 a 6.",
    commands=["dado", "dice"],
    usage="/dado 3",
    handle=dice_handle,
)
