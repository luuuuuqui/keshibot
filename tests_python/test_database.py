from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import takeshi_bot.database as database


class DatabaseTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.original_dir = database.DATABASE_DIR
        database.DATABASE_DIR = Path(self.temp.name)

    def tearDown(self) -> None:
        database.DATABASE_DIR = self.original_dir
        self.temp.cleanup()

    def test_group_activation_uses_inactive_groups_format(self) -> None:
        group_id = "123@g.us"

        self.assertTrue(database.is_active_group(group_id))
        database.deactivate_group(group_id)
        self.assertFalse(database.is_active_group(group_id))
        database.activate_group(group_id)
        self.assertTrue(database.is_active_group(group_id))

    def test_prefix_defaults_and_overrides(self) -> None:
        group_id = "123@g.us"

        self.assertEqual(database.get_prefix(group_id), "/")
        database.set_prefix(group_id, "!")
        self.assertEqual(database.get_prefix(group_id), "!")

    def test_spider_token_prefers_runtime_config(self) -> None:
        self.assertEqual(database.get_spider_api_token(), "seu_token_aqui")
        database.set_spider_api_token("secret-token")
        self.assertEqual(database.get_spider_api_token(), "secret-token")

    def test_restricted_message_types_have_code_default(self) -> None:
        types = database.read_restricted_message_types()
        self.assertEqual(types["image"], "imageMessage")
        self.assertEqual(types["lottieSticker"], "lottieStickerMessage")


if __name__ == "__main__":
    unittest.main()
