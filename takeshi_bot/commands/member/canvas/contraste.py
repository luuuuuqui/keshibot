from ._helpers import make_ffmpeg_image_command

command = make_ffmpeg_image_command(
    "contraste",
    ["contraste", "contrast", "melhora", "melhorar", "hd", "to-hd"],
    "Ajusta contraste da imagem.",
    "adjust_contrast",
)
