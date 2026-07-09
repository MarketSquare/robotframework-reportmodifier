# noqa: N999
from pathlib import Path
from typing import Optional

from reportmodifier.ReportModifier import ReportModifier
from robot.api.deco import not_keyword


class ReportModifierListener:
    """Listener der verwendet werden kann, um Ergebnise nach Jira zu übertragen.
    Voraussetzung: Der Robot-Testfallname entspricht dem Jira-Key.
    """

    ROBOT_LISTENER_API_VERSION = 3
    ROBOT_LIBRARY_SCOPE = "GLOBAL"

    def __init__(self, config_dir: Optional[str] = None) -> None:
        self._output_file: Optional[str] = None
        self._config_dir = config_dir

    @not_keyword
    def output_file(self, path: str) -> None:
        self._output_file = Path(path)

    def close(self) -> None:
        if self._output_file is None:
            failure_msg = "Output file is not set."
            raise TypeError(failure_msg)
        ReportModifier(
            self._output_file, self._output_file.parent, config_dir=self._config_dir
        ).write_report()
