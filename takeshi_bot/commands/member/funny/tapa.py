from ._helpers import make_action_command

command = make_action_command(
    "tapa",
    ["tapa", "slap"],
    "Da um tapa em um usuario.",
    "slap.mp4",
    "@{user} deu um tapa em @{target}!",
)
