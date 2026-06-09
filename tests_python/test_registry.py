from __future__ import annotations

import unittest
from pathlib import Path

from takeshi_bot.commands.registry import registry


class RegistryTest(unittest.TestCase):
    def test_expected_ported_commands_are_loaded(self) -> None:
        commands = {
            command.name
            for group in registry.all_commands().values()
            for command in group
        }
        expected = {
            "abrir",
            "anti-payment",
            "auto-sticker",
            "ban",
            "bratvid",
            "cep",
            "delete",
            "gerar-link",
            "get-group-id",
            "hide-tag",
            "info",
            "link-grupo",
            "perfil",
            "removebg",
            "saldo",
            "set-name",
            "to-mp3",
            "togif",
            "warn",
            "welcome",
            "yt-mp3",
        }
        self.assertTrue(expected.issubset(commands), expected - commands)

    def test_top_level_js_commands_have_python_counterpart(self) -> None:
        js_commands = {
            path.stem
            for folder in ("owner", "admin", "member")
            for path in Path("src", "commands", folder).glob("*.js")
        }
        py_modules = {
            path.stem.replace("_", "-")
            for path in Path("takeshi_bot", "commands").rglob("*.py")
            if path.name
            not in {"__init__.py", "base.py", "registry.py", "_helpers.py", "_restriction.py"}
        }
        self.assertEqual(sorted(js_commands - py_modules), [])

    def test_all_js_command_files_have_python_counterpart(self) -> None:
        js_commands = {
            path.relative_to("src/commands").with_suffix("").as_posix()
            for path in Path("src", "commands").rglob("*.js")
            if not path.name.startswith("\U0001f916")
        }
        py_modules = {
            path.relative_to("takeshi_bot/commands")
            .with_suffix("")
            .as_posix()
            .replace("_", "-")
            for path in Path("takeshi_bot", "commands").rglob("*.py")
            if path.name
            not in {"__init__.py", "base.py", "registry.py", "_helpers.py", "_restriction.py"}
        }
        self.assertEqual(sorted(js_commands - py_modules), [])


if __name__ == "__main__":
    unittest.main()
