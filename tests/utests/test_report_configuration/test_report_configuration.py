from pathlib import Path
import unittest
import mock
from src.reportmodifier._report_configuration import ReportConfiguration


class TestReportConfiguration(unittest.TestCase):
    def setUp(self) -> None:
        self.report = ReportConfiguration(Path(__file__).parent / 'configuration.yaml')

    def tearDown(self) -> None:
        pass

    def test_check_vt_config_wo_path_def(self):
        report = ReportConfiguration(Path(__file__).parent / 'vt.yaml')
        self.assertListEqual(report.keyword_names, ['Log', 'Compare Images'])

    def test_keyword_name_as_info(self):
        self.assertListEqual(self.report.names_as_info, ['Keyword Name As Info', 'Second Keyword As Info'])

    def test_reads_keyword_names_correctly(self):
        self.assertListEqual(self.report.keyword_names, ['Capture Page Screenshot', 'Take Screenshot', 'Log', 'Log'])

    def test_third_keyword(self):
        log_keyword = self.report.keywords[2]
        self.assertEqual(log_keyword.name, 'Log', 'Keyword name.')
        self.assertEqual(log_keyword.path, 'BuiltIn.Log', 'Keyword path.')
        self.assertListEqual(log_keyword.index, [1, 2], 'Keyword index.')

    def test_fourth_keyword(self):
        log_keyword = self.report.keywords[3]
        self.assertEqual(log_keyword.name, 'Log', 'Keyword name.')
        self.assertEqual(log_keyword.path, 'BuiltIn.Log', 'Keyword path.')
        self.assertListEqual(log_keyword.index, [1], 'Keyword index.')

    def test_message_pattern(self):
        report = ReportConfiguration(Path(__file__).parent / 'configuration.yaml')
        pattern = report.message_pattern
        self.assertListEqual(sorted(pattern), sorted(['.* Jobid is .*', 'Job .* with job id .* has sucessfully ended: MAXCC=.*']))

    def test_message_text(self):
        pattern = self.report.message_text
        self.assertListEqual(pattern, ['Relevanter Text'])

    def test_keyword_name_as_structure(self):
        self.assertEqual(1, len(self.report.keyword_as_structure))
        self.assertEqual(self.report.keyword_as_structure[0].name, 'Keyword Zum Zusammenklappen')


if __name__ == '__main__':
    unittest.main()
