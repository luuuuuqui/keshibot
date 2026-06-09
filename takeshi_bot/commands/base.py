from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from takeshi_bot.context import CommandContext

CommandHandler = Callable[["CommandContext"], Awaitable[None]]


@dataclass(frozen=True)
class Command:
    name: str
    description: str
    commands: list[str]
    usage: str
    handle: CommandHandler
