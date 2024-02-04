import unittest
from reportmodifier.ReportModifier import _check_name_relevance


class TestNameRelevance(unittest.TestCase):
    def setUp(self) -> None:
        self.maxDiff = None

    def test_empty_keywords(self):
        result = _check_name_relevance("test", [])
        self.assertEqual(result, [])

    def test_no_matching_keywords(self):
        result = _check_name_relevance(
            "test", [Keyword("not matching"), Keyword("also not matching")])
        self.assertEqual(result, [])

    def test_one_matching_keyword(self):
        result = _check_name_relevance("test", [Keyword(
            "not matching"), Keyword("test"), Keyword("also not matching")])
        self.assertEqual([t.name for t in result], ["test"])

    def test_multiple_matching_keywords(self):
        result = _check_name_relevance(
            "test", [
                Keyword("not matching"), 
                Keyword("test"), 
                Keyword("also not matching"),
                Keyword("TesT"), Keyword("TEST keyword with spaces")
            ])
        self.assertEqual([t.name for t in result], ["test", "TesT"])


class Keyword:
    def __init__(self, name):
        self.name = name


if __name__ == '__main__':
    unittest.main()
