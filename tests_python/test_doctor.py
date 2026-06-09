from __future__ import annotations

import unittest

from takeshi_bot.doctor import _command_mapping


class DoctorTest(unittest.TestCase):
    def test_command_mapping_is_complete(self) -> None:
        ok, detail = _command_mapping()
        self.assertTrue(ok, detail)


if __name__ == "__main__":
    unittest.main()
