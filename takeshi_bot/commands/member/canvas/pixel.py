from ._helpers import make_ffmpeg_image_command

command = make_ffmpeg_image_command(
    "pixel",
    ["pixel", "pixelar", "pixelate"],
    "Aplica efeito pixelado na imagem.",
    "apply_pixelation",
)
