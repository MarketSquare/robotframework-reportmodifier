import unittest
from unittest import mock
from reportmodifier.ReportModifier import _check_index_relevance


class TestCheckIndexRelevance(unittest.TestCase):

    def setUp(self):
        self.keyword_one = mock.MagicMock()
        self.keyword_one.index = [1]

        self.keyword_two = mock.MagicMock()
        self.keyword_two.index = [2]
        self.keywords = [self.keyword_one, self.keyword_two]

    def test_index_is_none(self):
        self.keyword_one.index = None
        filtered_keywords = _check_index_relevance(0, self.keywords)
        self.assertListEqual([self.keyword_one], filtered_keywords)

    def test_index_is_not_relevant(self):
        filtered_keywords = _check_index_relevance(0, self.keywords)
        self.assertListEqual([], filtered_keywords)

    def test_index_is_relevant(self):
        filtered_keywords = _check_index_relevance(2, self.keywords)
        self.assertListEqual([self.keyword_two], filtered_keywords)


if __name__ == '__main__':
    unittest.main()
