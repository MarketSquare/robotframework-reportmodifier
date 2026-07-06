import unittest
from unittest import mock

from src.reportmodifier.ReportModifierVisitor import _message_is_under_ignored_keyword


class TestMessageIsUnderIgnoredKeyword(unittest.TestCase):
    def setUp(self):
        self.msg = mock.MagicMock()

    def test_no_ignored_keywords(self):
        self.assertFalse(_message_is_under_ignored_keyword(self.msg, []))

    def test_message_is_under_ignored_keyword(self):
        with mock.patch(
            "src.reportmodifier.ReportModifierVisitor._get_keyword_call_path",
            return_value="Test.Run Keyword And Ignore Error.Fail",
        ):
            self.assertTrue(_message_is_under_ignored_keyword(self.msg, ["Run Keyword And Ignore Error"]))

    def test_message_is_not_under_ignored_keyword(self):
        with mock.patch(
            "src.reportmodifier.ReportModifierVisitor._get_keyword_call_path",
            return_value="Test.Some Keyword.Log",
        ):
            self.assertFalse(_message_is_under_ignored_keyword(self.msg, ["Run Keyword And Ignore Error"]))


if __name__ == "__main__":
    unittest.main()
