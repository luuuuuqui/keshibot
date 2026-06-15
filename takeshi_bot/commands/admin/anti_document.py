from ._restriction import make_restriction_command

command = make_restriction_command(
    "anti-document",
    ["anti-document", "anti-documento", "anti-doc", "anti-documentos"],
    "anti-document",
    "Apaga documentos quando ativo.",
)
