from ._helpers import make_ffmpeg_image_command

command = make_ffmpeg_image_command(
    "espelhar",
    ["espelhar", "muda-direcao", "mudar-direcao", "mirror", "espelho"],
    "Espelha a imagem enviada.",
    "mirror_image",
)
