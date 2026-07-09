import unittest
from pathlib import Path

from src.reportmodifier.ReportModifierVisitor import _default_config_dir


class TestDefaultConfigDir(unittest.TestCase):
    def test_returns_tests_folder(self):
        source = Path("C:/repo/tests/atests/suite.robot")
        self.assertEqual(_default_config_dir(source), Path("C:/repo/tests"))

    def test_uses_first_tests_folder(self):
        source = Path("/home/user/tests/nested/tests/suite.robot")
        self.assertEqual(_default_config_dir(source), Path("/home/user/tests"))

    def test_returns_none_without_tests_folder(self):
        source = Path("/home/user/suites/suite.robot")
        self.assertIsNone(_default_config_dir(source))

    def test_returns_none_for_missing_source(self):
        self.assertIsNone(_default_config_dir(None))


if __name__ == "__main__":
    unittest.main()
