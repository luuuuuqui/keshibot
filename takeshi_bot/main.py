from __future__ import annotations

import asyncio

from .bridge import BaileysBridge
from .loader import load
from .logger import banner_log, configure_logging, info_log, success_log
from .paths import ensure_runtime_dirs


async def async_main() -> None:
    ensure_runtime_dirs()
    configure_logging()
    banner_log()
    info_log("Iniciando Takeshi Bot Python...")
    bridge = BaileysBridge()
    await bridge.start()
    success_log("Bridge Baileys iniciado. Aguardando eventos...")
    try:
        await load(bridge)
    finally:
        await bridge.stop()


def main() -> None:
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
