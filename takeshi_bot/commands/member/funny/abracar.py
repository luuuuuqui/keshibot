from ._helpers import make_action_command

command = make_action_command(
    "abracar",
    ["abracar", "abraca", "abraco", "abracos"],
    "Abraca um usuario.",
    "hug-darker-than-black.mp4",
    "@{user} deu um abraco apaixonante em @{target}!",
)
