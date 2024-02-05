import unittest
from src.reportmodifier.ReportModifier import _keyword_name_for_structure_is_relevant


class TestPathRelevance(unittest.TestCase):
    def setUp(self):
        pass

    def test_name_is_relevant(self):
        self.assertTrue(_keyword_name_for_structure_is_relevant('Name', ['Name']))
        self.assertTrue(_keyword_name_for_structure_is_relevant('Name', ['name']))
        self.assertTrue(_keyword_name_for_structure_is_relevant('Name', [' name ']))

    def test_name_is_not_relevant(self):
        self.assertFalse(_keyword_name_for_structure_is_relevant('Nicht relevant', ['relevant']))


if __name__ == '__main__':
    unittest.main()
