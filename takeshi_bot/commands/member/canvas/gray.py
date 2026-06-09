from ._helpers import make_ffmpeg_image_command

command = make_ffmpeg_image_command(
    "gray",
    ["gray", "cinza", "grayscale"],
    "Converte a imagem para tons de cinza.",
    "convert_to_grayscale",
)
