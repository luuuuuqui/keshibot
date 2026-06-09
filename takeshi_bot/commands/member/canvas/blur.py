from ._helpers import make_ffmpeg_image_command

command = make_ffmpeg_image_command(
    "blur",
    ["blur", "embaca", "embacar"],
    "Embaca a imagem enviada.",
    "apply_blur",
)
