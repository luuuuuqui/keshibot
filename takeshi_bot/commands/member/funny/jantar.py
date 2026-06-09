from ._helpers import make_action_command

command = make_action_command(
    "jantar",
    ["jantar", "dinner"],
    "Chama um usuario para jantar.",
    "dinner.mp4",
    "@{user} chamou @{target} para jantar!",
)
