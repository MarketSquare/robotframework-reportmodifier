import unittest

from unittest import mock
from unittest.mock import patch
from src.reportmodifier.ReportModifierVisitor import _check_path_relevance


class TestPathRelevance(unittest.TestCase):
    def setUp(self):
        self.keyword_one = mock.MagicMock()
        self.keyword_one.kwname = "foo"
        self.keyword_one.path = "test.foo"
    
        self.keyword_two = mock.MagicMock()
        self.keyword_two.kwname = "bar"
        self.keyword_two.path = "path.with.bar"
        self.keywords = [self.keyword_one, self.keyword_two]

    def test_path_is_not_relevant(self):
        with mock.patch('src.reportmodifier.ReportModifierVisitor._get_keyword_call_path',
                        return_value='some.path.with.Foo'):

            filtered_keywords = _check_path_relevance(self.keyword_one, self.keywords)
            self.assertListEqual([], filtered_keywords)
            
    @patch('src.reportmodifier.ReportModifierVisitor._get_keyword_call_path',
           return_value='some.other.path.with.bar')
    def test_path_is_relevant(self, patched):
        filtered_keywords = _check_path_relevance(self.keyword_two, self.keywords)
        assert patched.call_count == 1
        self.assertListEqual([self.keyword_two], filtered_keywords)

    def test_path_is_none(self):
        with mock.patch('src.reportmodifier.ReportModifierVisitor._get_keyword_call_path',
                        return_value='path.with.bar'):
            self.keyword_two.path = None
            filtered_keywords = _check_path_relevance(self.keyword_two, self.keywords)
            self.assertListEqual([self.keyword_two], filtered_keywords)


if __name__ == '__main__':
    unittest.main()
