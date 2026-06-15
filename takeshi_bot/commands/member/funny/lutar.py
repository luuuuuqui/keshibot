from ._helpers import make_action_command

command = make_action_command(
    "lutar",
    ["lutar", "luta", "fight"],
    "Luta com um usuario.",
    "fight.mp4",
    "@{user} entrou em combate com @{target}!",
)
