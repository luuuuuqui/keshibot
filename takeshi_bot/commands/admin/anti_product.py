from ._restriction import make_restriction_command

command = make_restriction_command(
    "anti-product",
    ["anti-product", "anti-produto", "anti-produtos"],
    "anti-product",
    "Apaga mensagens de produto quando ativo.",
)
