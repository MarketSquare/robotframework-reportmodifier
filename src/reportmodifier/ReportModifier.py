from pathlib import Path
from typing import Union

from robot.reporting import ResultWriter
from robot.result import ExecutionResult

from .ReportModifierVisitor import ReportModifierVisitor


class ReportModifier:
    """Creates an additional log filtering the content based on yaml-configurations

        Args:
            basis_output_xml (Union[Path, str]): path for the source xml file
            result_dir (Union[Path, str]): output dir path
            report_name (str): optionally, target report name
    """

    def __init__(self,
                 basis_output_xml: Union[Path, str],
                 result_dir: Union[Path, str],
                 report_name: str):
        self._basis_output_xml = basis_output_xml
        self._result_dir = result_dir
        self._modifier = ReportModifierVisitor()
        self._modifier.report_name = report_name
        self._execution_result = ExecutionResult(self._basis_output_xml)

    def write_report(self) -> None:
        """Creates an additional log filtering the content based on yaml-configurations

        The yaml-configuration needs to be set as test tag. It's possible to define a basic configuration, 
        therefore "report:basic_config needs to be set as tag and basic_config.yaml-file must be stored in ./tests folder
        """
        self._execution_result.visit(self._modifier)
        if self._modifier.report_configuration is not None:
            ResultWriter(self._execution_result).write_results(
                outputdir=self._result_dir,
                log=f'{self._modifier.report_name}.html',
                report=None,
                expandkeywords="NAME:.*"
            )
