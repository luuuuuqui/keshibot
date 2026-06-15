from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from takeshi_bot.services.ffmpeg import Ffmpeg


class RecordingFfmpeg(Ffmpeg):
    def __init__(self, temp_dir: Path) -> None:
        super().__init__(temp_dir)
        self.calls: list[tuple[str, ...]] = []

    async def _execute(self, *args: str) -> None:
        self.calls.append(args)
        Path(args[-1]).write_bytes(b"output")


class FfmpegServiceTest(unittest.IsolatedAsyncioTestCase):
    async def test_js_canvas_filters_are_ported(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ffmpeg = RecordingFfmpeg(Path(tmp))
            input_path = str(Path(tmp) / "input.png")

            blur = await ffmpeg.apply_blur(input_path)
            gray = await ffmpeg.convert_to_grayscale(input_path)
            mirror = await ffmpeg.mirror_image(input_path)
            contrast = await ffmpeg.adjust_contrast(input_path)
            pixel = await ffmpeg.apply_pixelation(input_path)
            sticker = await ffmpeg.convert_sticker_to_image(input_path)

            self.assertTrue(blur.endswith(".png"))
            self.assertTrue(gray.endswith(".png"))
            self.assertTrue(mirror.endswith(".png"))
            self.assertTrue(contrast.endswith(".png"))
            self.assertTrue(pixel.endswith(".png"))
            self.assertTrue(sticker.endswith(".png"))
            self.assertIn(("-i", input_path, "-vf", "boxblur=7:5", blur), ffmpeg.calls)
            self.assertIn(("-i", input_path, "-vf", "format=gray", gray), ffmpeg.calls)
            self.assertIn(("-i", input_path, "-vf", "hflip", mirror), ffmpeg.calls)
            self.assertIn(("-i", input_path, "-vf", "eq=contrast=1.2", contrast), ffmpeg.calls)
            self.assertIn(
                (
                    "-i",
                    input_path,
                    "-vf",
                    "scale=iw/6:ih/6, scale=iw*10:ih*10:flags=neighbor",
                    pixel,
                ),
                ffmpeg.calls,
            )
            self.assertIn(("-i", input_path, sticker), ffmpeg.calls)

    async def test_media_conversion_helpers_are_available(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ffmpeg = RecordingFfmpeg(Path(tmp))
            input_path = str(Path(tmp) / "input.mp4")

            audio = await ffmpeg.extract_audio_to_mp3(input_path)
            image = await ffmpeg.normalize_image(input_path)
            video = await ffmpeg.copy_video(input_path)

            self.assertTrue(audio.endswith(".mp3"))
            self.assertTrue(image.endswith(".jpg"))
            self.assertTrue(video.endswith(".mp4"))
            self.assertIn(
                (
                    "-i",
                    input_path,
                    "-vn",
                    "-acodec",
                    "libmp3lame",
                    "-f",
                    "mp3",
                    "-ar",
                    "44100",
                    "-ac",
                    "2",
                    "-b:a",
                    "128k",
                    audio,
                ),
                ffmpeg.calls,
            )
            self.assertIn(("-i", input_path, "-q:v", "2", image), ffmpeg.calls)
            self.assertIn(("-i", input_path, "-c", "copy", video), ffmpeg.calls)


if __name__ == "__main__":
    unittest.main()
