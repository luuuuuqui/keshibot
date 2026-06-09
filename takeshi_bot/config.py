from __future__ import annotations

import os

from .paths import ASSETS_DIR, COMMANDS_DIR, DATABASE_DIR, TEMP_DIR

PREFIX = os.getenv("TAKESHI_PREFIX", "/")
BOT_EMOJI = os.getenv("TAKESHI_BOT_EMOJI", "\U0001f916")
BOT_NAME = os.getenv("TAKESHI_BOT_NAME", "Takeshi Bot")

BOT_LID = os.getenv("TAKESHI_BOT_LID", "12345678901234567890@lid")
OWNER_LID = os.getenv("TAKESHI_OWNER_LID", "12345678901234567890@lid")

TIMEOUT_IN_MILLISECONDS_BY_EVENT = int(
    os.getenv("TAKESHI_TIMEOUT_IN_MILLISECONDS_BY_EVENT", "500")
)

SPIDER_API_BASE_URL = os.getenv(
    "SPIDER_API_BASE_URL", "https://api.spiderx.com.br/api"
)
SPIDER_API_TOKEN = os.getenv("SPIDER_API_TOKEN", "seu_token_aqui")

LINKER_BASE_URL = os.getenv("LINKER_BASE_URL", "https://linker.devgui.dev/api")
LINKER_API_KEY = os.getenv("LINKER_API_KEY", "seu_token_aqui")

ONLY_GROUP_ID = os.getenv("TAKESHI_ONLY_GROUP_ID", "")
DEVELOPER_MODE = os.getenv("TAKESHI_DEVELOPER_MODE", "").lower() in {
    "1",
    "true",
    "sim",
    "yes",
    "on",
}

PROXY_PROTOCOL = os.getenv("PROXY_PROTOCOL", "http")
PROXY_HOST = os.getenv("PROXY_HOST", "")
PROXY_PORT = os.getenv("PROXY_PORT", "")
PROXY_USERNAME = os.getenv("PROXY_USERNAME", "")
PROXY_PASSWORD = os.getenv("PROXY_PASSWORD", "")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

__all__ = [
    "ASSETS_DIR",
    "BOT_EMOJI",
    "BOT_LID",
    "BOT_NAME",
    "COMMANDS_DIR",
    "DATABASE_DIR",
    "DEVELOPER_MODE",
    "LINKER_API_KEY",
    "LINKER_BASE_URL",
    "ONLY_GROUP_ID",
    "OPENAI_API_KEY",
    "OWNER_LID",
    "PREFIX",
    "PROXY_HOST",
    "PROXY_PASSWORD",
    "PROXY_PORT",
    "PROXY_PROTOCOL",
    "SPIDER_API_BASE_URL",
    "SPIDER_API_TOKEN",
    "TEMP_DIR",
    "TIMEOUT_IN_MILLISECONDS_BY_EVENT",
]
