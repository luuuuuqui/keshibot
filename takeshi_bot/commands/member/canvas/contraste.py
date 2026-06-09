from ._helpers import make_ffmpeg_image_command

command = make_ffmpeg_image_command(
    "contraste",
    ["contraste", "contrast"],
    "Ajusta contraste da imagem.",
    "adjust_contrast",
)
