from ._restriction import make_restriction_command

command = make_restriction_command(
    "anti-event",
    ["anti-event", "anti-evento", "anti-eventos"],
    "anti-event",
    "Apaga mensagens de evento quando ativo.",
)
