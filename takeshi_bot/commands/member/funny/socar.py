from ._helpers import make_action_command

command = make_action_command(
    "socar",
    ["socar", "soco", "punch"],
    "Da um soco em um usuario.",
    "punch.mp4",
    "@{user} deu um soco em @{target}!",
)
