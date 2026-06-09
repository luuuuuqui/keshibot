from ._restriction import make_restriction_command

command = make_restriction_command(
    "anti-status-grupo",
    ["anti-status-grupo", "anti-status", "antistatus"],
    "anti-status-grupo",
    "Remove mensagens de status no grupo.",
)
