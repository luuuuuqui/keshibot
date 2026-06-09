from __future__ import annotations

from takeshi_bot import config


def _require_key() -> str:
    key = config.LINKER_API_KEY
    if not key or key.strip() == "" or key == "seu_token_aqui":
        raise RuntimeError("API Key do Linker nao configurada!")
    return key


async def upload(image_buffer: bytes, filename: str) -> str:
    import httpx

    if not image_buffer:
        raise RuntimeError("O buffer da imagem esta vazio!")
    files = {"file": (filename, image_buffer, "image/jpeg")}
    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(
            f"{config.LINKER_BASE_URL}/upload",
            headers={"X-API-Key": _require_key()},
            files=files,
        )
        response.raise_for_status()
        data = response.json()
    if not data.get("url"):
        raise RuntimeError(f"Erro na API: {data.get('error', 'Erro desconhecido')}")
    return data["url"]
