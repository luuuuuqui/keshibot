from ._helpers import make_action_command

command = make_action_command(
    "matar",
    ["matar", "kill"],
    "Brinca de matar um usuario.",
    "kill.mp4",
    "@{user} eliminou @{target} nessa brincadeira!",
)
