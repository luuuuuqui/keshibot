from __future__ import annotations

from typing import Any
from urllib.parse import quote

from takeshi_bot import config
from takeshi_bot.database import get_spider_api_token


def _require_token() -> str:
    token = get_spider_api_token()
    if not token or token.strip() == "" or token == "seu_token_aqui":
        raise RuntimeError(
            "Token da API do Spider X nao configurado. Configure em config.py "
            f"ou use {config.PREFIX}set-spider-api-token seu_token_aqui."
        )
    return token


async def _get(path: str, params: dict[str, Any]) -> Any:
    import httpx

    params = {**params, "api_key": _require_token()}
    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.get(f"{config.SPIDER_API_BASE_URL}{path}", params=params)
        response.raise_for_status()
        return response.json()


async def _post(path: str, json_body: dict[str, Any]) -> Any:
    import httpx

    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(
            f"{config.SPIDER_API_BASE_URL}{path}",
            params={"api_key": _require_token()},
            json=json_body,
        )
        response.raise_for_status()
        return response.json()


async def play(media_type: str, search: str) -> Any:
    if not search:
        raise RuntimeError("Voce precisa informar o que deseja buscar!")
    return await _get(f"/downloads/play-{media_type}", {"search": search})


async def download(media_type: str, url: str) -> Any:
    if not url:
        raise RuntimeError("Voce precisa informar uma URL do que deseja buscar!")
    return await _get(f"/downloads/{media_type}", {"url": url})


async def pinterest(search_text: str) -> Any:
    if not search_text:
        raise RuntimeError("Voce precisa informar o parametro de pesquisa!")
    return await _get("/downloads/pinterest", {"search": search_text})


async def search(search_type: str, search_text: str) -> Any:
    if not search_text:
        raise RuntimeError("Voce precisa informar o parametro de pesquisa!")
    return await _get(f"/search/{search_type}", {"search": search_text})


async def gemini(text: str) -> str:
    data = await _post("/ai/gemini", {"text": text})
    return data.get("response", "")


async def gpt5_mini(text: str) -> str:
    data = await _post("/ai/gpt-5-mini", {"text": text})
    return data.get("response", "")


async def deepseek_v4_flash(text: str) -> str:
    data = await _post("/ai/deepseek-v4-flash", {"text": text})
    return data.get("response", "")


async def image_ai(description: str) -> Any:
    if not description:
        raise RuntimeError("Voce precisa informar a descricao da imagem!")
    return await _get("/ai/flux", {"text": description})


def canvas_url(kind: str, image_url: str) -> str:
    if not image_url:
        raise RuntimeError("Voce precisa informar a URL da imagem!")
    return (
        f"{config.SPIDER_API_BASE_URL}/canvas/{kind}?image_url={quote(image_url)}"
        f"&api_key={_require_token()}"
    )


def sticker_url(kind: str, text: str) -> str:
    if not text:
        raise RuntimeError("Voce precisa informar o parametro de texto!")
    return (
        f"{config.SPIDER_API_BASE_URL}/stickers/{kind}?text={quote(text)}"
        f"&api_key={_require_token()}"
    )


async def to_gif(buffer: bytes) -> str:
    import httpx

    if not buffer:
        raise RuntimeError("Voce precisa informar o buffer do arquivo!")
    files = {"file": ("sticker.webp", buffer, "image/webp")}
    async with httpx.AsyncClient(timeout=90) as client:
        response = await client.post(
            f"{config.SPIDER_API_BASE_URL}/utilities/to-gif",
            params={"api_key": _require_token()},
            files=files,
        )
        response.raise_for_status()
        data = response.json()
    return data.get("url", "")


async def remove_bg(buffer: bytes, mime_type: str = "image/png", filename: str = "image.png") -> bytes:
    import httpx

    if not buffer:
        raise RuntimeError("Voce precisa informar o buffer da imagem!")
    files = {"image": (filename, buffer, mime_type)}
    async with httpx.AsyncClient(timeout=90) as client:
        response = await client.post(
            f"{config.SPIDER_API_BASE_URL}/removebg",
            params={"api_key": _require_token()},
            files=files,
        )
        response.raise_for_status()
        return response.content


async def set_proxy(name: str) -> bool:
    if not name:
        raise RuntimeError("Voce precisa informar o nome da nova proxy!")
    data = await _post("/internal/set-node-js-proxy-active", {"name": name})
    return bool(data.get("success"))
