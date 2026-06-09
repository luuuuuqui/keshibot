from __future__ import annotations

import unittest

from takeshi_bot.utils import extract_data_from_message, format_command, split_by_characters


class UtilsTest(unittest.TestCase):
    def test_format_command_removes_accents_and_symbols(self) -> None:
        self.assertEqual(format_command(" /MEnu! "), "menu")
        self.assertEqual(format_command("\u00e1\u00e9\u00ed\u00f3\u00fa \u00e7"), "aeiouc")

    def test_split_by_multiple_command_separators(self) -> None:
        self.assertEqual(
            split_by_characters("um / dois | tres \\ quatro", ["\\", "|", "/"]),
            ["um", "dois", "tres", "quatro"],
        )

    def test_extract_text_command(self) -> None:
        data = extract_data_from_message(
            {
                "key": {
                    "remoteJid": "123@g.us",
                    "participant": "999@lid",
                },
                "message": {"conversation": "/ping agora"},
            }
        )

        self.assertEqual(data["remote_jid"], "123@g.us")
        self.assertEqual(data["prefix"], "/")
        self.assertEqual(data["command_name"], "ping")
        self.assertEqual(data["full_args"], "agora")
        self.assertEqual(data["user_lid"], "999@lid")


if __name__ == "__main__":
    unittest.main()
