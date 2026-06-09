from __future__ import annotations

import asyncio
import random
from pathlib import Path

from takeshi_bot.paths import TEMP_DIR
from takeshi_bot.utils import remove_file_if_exists


class Ffmpeg:
    def __init__(self, temp_dir: Path = TEMP_DIR) -> None:
        self.temp_dir = temp_dir
        self.temp_dir.mkdir(parents=True, exist_ok=True)

    async def _execute(self, *args: str) -> None:
        process = await asyncio.create_subprocess_exec(
            "ffmpeg",
            "-y",
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        _, stderr = await process.communicate()
        if process.returncode != 0:
            raise RuntimeError(stderr.decode("utf-8", errors="replace"))

    def _temp_path(self, extension: str = "png") -> Path:
        return self.temp_dir / f"{random.randint(10_000, 99_999)}.{extension}"

    async def apply_blur(self, input_path: str, intensity: str = "7:5") -> str:
        output = self._temp_path()
        await self._execute("-i", input_path, "-vf", f"boxblur={intensity}", str(output))
        return str(output)

    async def convert_to_grayscale(self, input_path: str) -> str:
        output = self._temp_path()
        await self._execute("-i", input_path, "-vf", "format=gray", str(output))
        return str(output)

    async def mirror_image(self, input_path: str) -> str:
        output = self._temp_path()
        await self._execute("-i", input_path, "-vf", "hflip", str(output))
        return str(output)

    async def adjust_contrast(self, input_path: str, contrast: float = 1.2) -> str:
        output = self._temp_path()
        await self._execute("-i", input_path, "-vf", f"eq=contrast={contrast}", str(output))
        return str(output)

    async def apply_pixelation(self, input_path: str) -> str:
        output = self._temp_path()
        await self._execute(
            "-i",
            input_path,
            "-vf",
            "scale=iw/6:ih/6, scale=iw*10:ih*10:flags=neighbor",
            str(output),
        )
        return str(output)

    async def convert_sticker_to_image(self, input_path: str) -> str:
        output = self._temp_path()
        await self._execute("-i", input_path, str(output))
        return str(output)

    async def extract_audio_to_mp3(self, input_path: str) -> str:
        output = self._temp_path("mp3")
        await self._execute(
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
            str(output),
        )
        return str(output)

    async def normalize_image(self, input_path: str, extension: str = "jpg") -> str:
        output = self._temp_path(extension)
        await self._execute("-i", input_path, "-q:v", "2", str(output))
        return str(output)

    async def copy_video(self, input_path: str) -> str:
        output = self._temp_path("mp4")
        await self._execute("-i", input_path, "-c", "copy", str(output))
        return str(output)

    async def cleanup(self, file_path: str | None) -> None:
        if file_path:
            remove_file_if_exists(file_path)
