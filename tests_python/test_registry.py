from __future__ import annotations

import re
import unittest
from pathlib import Path

from takeshi_bot.commands.registry import registry
from takeshi_bot.utils import format_command


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

    def test_js_command_aliases_are_registered_in_python(self) -> None:
        py_aliases = {
            format_command(alias)
            for group in registry.all_commands().values()
            for command in group
            for alias in command.commands
        }
        missing: list[str] = []
        for path in Path("src", "commands").rglob("*.js"):
            if "como-criar-comandos" in path.name:
                continue
            relative = path.relative_to("src/commands").with_suffix("").as_posix()
            for alias in self._js_command_aliases(path):
                if format_command(alias) not in py_aliases:
                    missing.append(f"{relative}: {alias}")
        self.assertEqual(missing, [])

    def test_example_aliases_match_advanced_js_examples(self) -> None:
        expected = {
            "enviar-botao": "enviar-botoes",
            "botoes-exemplo": "enviar-botoes",
            "lista-exemplo": "enviar-lista",
            "enviar-list": "enviar-lista",
            "poll-example": "enviar-enquete",
            "exemplo-poll": "enviar-enquete",
            "codigo": "enviar-codigo",
            "latex": "enviar-latex",
            "formula": "enviar-latex",
            "reels": "enviar-reels",
            "rich-reels": "enviar-reels",
            "tabela": "enviar-tabela",
            "texto-colorido": "enviar-texto-colorido",
            "rich-texto": "enviar-texto-colorido",
            "gatilho-exemplo": "exemplo-gatilho",
            "raw": "raw-message",
            "metadados": "obter-metadados-mensagem",
            "info-msg": "obter-metadados-mensagem",
        }
        for alias, command_name in expected.items():
            with self.subTest(alias=alias):
                match = registry.find(alias)
                self.assertIsNotNone(match.command)
                self.assertEqual(match.command.name, command_name)

    @staticmethod
    def _js_command_aliases(path: Path) -> list[str]:
        text = path.read_text(encoding="utf-8", errors="replace")
        match = re.search(r"commands\s*:\s*\[([\s\S]*?)\]", text)
        if not match:
            return []
        return re.findall(r"['\"]([^'\"]+)['\"]", match.group(1))


if __name__ == "__main__":
    unittest.main()
