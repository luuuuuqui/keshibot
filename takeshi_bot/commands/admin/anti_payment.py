from ._restriction import make_restriction_command

command = make_restriction_command(
    "anti-payment",
    ["anti-payment", "anti-pagamento", "anti-cobranca"],
    "anti-payment",
    "Remove usuarios que enviam cobrancas.",
)
