from __future__ import annotations

import importlib
import pkgutil
from dataclasses import dataclass

from takeshi_bot.commands.base import Command
from takeshi_bot.utils import format_command


@dataclass(frozen=True)
class CommandMatch:
    type: str
    command: Command | None


class CommandRegistry:
    def __init__(self) -> None:
        self._loaded = False
        self._commands: dict[str, list[Command]] = {}

    def load(self) -> None:
        if self._loaded:
            return
        for command_type in ("owner", "admin", "member"):
            package_name = f"takeshi_bot.commands.{command_type}"
            package = importlib.import_module(package_name)
            commands: list[Command] = []
            for module_info in pkgutil.walk_packages(package.__path__, package.__name__ + "."):
                if module_info.ispkg:
                    continue
                module = importlib.import_module(module_info.name)
                command = getattr(module, "command", None)
                if isinstance(command, Command):
                    commands.append(command)
            self._commands[command_type] = commands
        self._loaded = True

    def find(self, command_name: str) -> CommandMatch:
        self.load()
        formatted = format_command(command_name)
        for command_type, commands in self._commands.items():
            for command in commands:
                aliases = [format_command(alias) for alias in command.commands]
                if formatted in aliases:
                    return CommandMatch(command_type, command)
        return CommandMatch("", None)

    def all_commands(self) -> dict[str, list[Command]]:
        self.load()
        return self._commands


registry = CommandRegistry()
