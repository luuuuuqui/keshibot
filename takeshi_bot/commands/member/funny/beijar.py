from ._helpers import make_action_command

command = make_action_command(
    "beijar",
    ["beijar", "beija", "beijo"],
    "Beija um usuario.",
    "kiss.mp4",
    "@{user} deu um beijo em @{target}!",
)
