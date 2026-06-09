from ._restriction import make_restriction_command

command = make_restriction_command(
    "anti-audio",
    ["anti-audio", "anti-audios"],
    "anti-audio",
    "Apaga audios quando ativo.",
)
