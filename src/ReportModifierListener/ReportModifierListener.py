from collections import defaultdict
from pathlib import Path
from typing import Dict, Optional
import robot.result
import robot.running
from robot.api.deco import not_keyword

from reportmodifier.ReportModifier import ReportModifier


class JiraTestreportSplitter:
    """ Listener der verwendet werden kann, um Ergebnise nach Jira zu übertragen. 
    Voraussetzung: Der Robot-Testfallname entspricht dem Jira-Key.
    """
    ROBOT_LISTENER_API_VERSION = 3
    ROBOT_LIBRARY_SCOPE = "GLOBAL"

    def __init__(self) -> None:
        self.ROBOT_LIBRARY_LISTENER = self
        self._jira_testcases: Dict[str,
                                   robot.result.TestCase] = defaultdict(list)
        self._output_file: Optional[str] = None

    @not_keyword
    def end_test(self, test: robot.running.TestCase, result: robot.result.TestCase) -> None:
        self._jira_testcases[test.name].append(result)

    @not_keyword
    def output_file(self, path: str) -> None:
        self._output_file = Path(path)

    def close(self) -> None:
        ReportModifier(
              self._output_file,
              self._output_file.parent
        )
