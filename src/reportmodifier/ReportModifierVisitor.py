# noqa: N999
from collections import defaultdict
from copy import deepcopy
from pathlib import Path

import regex
from robot.api import logger
from robot.model import TestSuite
from robot.result import Keyword, Message, ResultVisitor, TestCase

from ._file_tools import get_files_in_folder
from ._report_configuration import ReportConfiguration


class ReportModifierVisitor(ResultVisitor):
    def __init__(self) -> None:
        super().__init__()
        self.report_configuration = ReportConfiguration(None)
        self.basic_configuration = ReportConfiguration(None)
        self.__report_name = None
        self.__keyword_calls = defaultdict(int)
        self._relevant_keyword_calls = []
        self._relevant_messages = defaultdict(list)
        self._keyword = None
        self._keyword_path = ""
        self.__root = None
        self._tests = []

    @property
    def report_name(self):
        if self.__report_name is None:
            return "custom_log"
        return self.__report_name

    @report_name.setter
    def report_name(self, name):
        self.__report_name = name

    def start_suite(self, suite: TestSuite) -> bool | None:
        if self.__root is None:
            self.__root = suite
        if suite.has_setup:
            suite.setup = None

    def end_suite(self, suite: TestSuite):
        if suite.name == self.__root.name:
            suite.suites.clear()
            suite.tests.clear()
            suite.tests = self._tests
        if suite.has_teardown:
            suite.teardown = None

    def start_test(self, test: TestCase):
        self._relevant_messages = defaultdict(list)
        self._relevant_keyword_calls = []
        self.report_configuration = ReportConfiguration(None)
        for tag in test.tags:
            if tag.startswith(("fb_report:", "report:")):
                report_configuration = tag.split("report:")[-1].strip()
                test_path = Path(test.source)
                test_dir = Path(*test_path.parts[0 : test_path.parts.index("tests") + 1])
                configuration_path = get_files_in_folder(
                    top_level_dir=test_dir,
                    condition_callback=lambda p: Path(p).stem.lower() == report_configuration.split(".yaml")[0].lower()  # noqa: B023
                    and Path(p).suffix == ".yaml",
                    recursive=True,
                )
                if not configuration_path:
                    logger.error(
                        f'Could not find custon log configuration "{report_configuration}" of test  {test.name}',
                    )
                    return False
                path = list(configuration_path.values())[0]
                logger.info(f"Found log configuration of fest: {test.name}: {tag} {path}")
                if report_configuration.lower() == "basic_config":
                    self.basic_configuration = ReportConfiguration(path)
                else:
                    self.report_configuration = ReportConfiguration(path)
                    if self.__report_name is None:
                        self.__report_name = report_configuration
                break

    def end_test(self, test: TestCase):
        if self.report_configuration or self.basic_configuration:
            test.body.clear()
            for keyword, messages in self._relevant_messages.items():
                if keyword and messages:
                    keyword.libname = ""
                    keyword.assign = ""
                    keyword.args = []
                    keyword.body = messages
                    test.body.append(keyword)
                else:
                    test.body += messages
            test.setup = None
            test.teardown = None
            logger.debug(f"Relevant keywords: {self._relevant_keyword_calls}")
        self._tests.append(deepcopy(test))

    def start_keyword(self, keyword: Keyword):
        if self.report_configuration or self.basic_configuration:
            logger.debug(f"Checking {keyword.kwname} --> {keyword.libname} --> {keyword.parent.name}")
            self.__keyword_calls[keyword.kwname] += 1
            if _keyword_name_for_structure_is_relevant(
                keyword.kwname,
                [k.name for k in self.report_configuration.keyword_as_structure],
            ):
                self._keyword = keyword
                self._keyword_path = _get_keyword_call_path(keyword)
            if _keyword_name_as_info_is_relevant(keyword, self.report_configuration, self.basic_configuration):
                msg = f'<b><mark style="background:powderblue">{keyword.name.strip()}</mark></b>\n{keyword.doc.strip()}'
                message = Message(msg, level="INFO", html=True, timestamp=keyword.starttime)
                self._relevant_messages[self._keyword].append(message)
                self._relevant_keyword_calls.append(_get_keyword_call_path(keyword))
            if _all_keyword_messages_are_relevant(
                keyword,
                self.__keyword_calls[keyword.kwname],
                self._relevant_messages[self._keyword],
                self.report_configuration,
                self.basic_configuration,
            ):
                logger.debug(f"Found relevant keyword {keyword.kwname}")
                last_message = _get_last_message(self._relevant_messages[self._keyword])
                submessages = []
                submessages = _get_all_submessages(keyword.body, submessages)
                relevant_messages = [
                    m
                    for m in keyword.messages + submessages
                    if not _message_shall_be_ignored(
                        m.message,
                        self.report_configuration,
                        self.basic_configuration,
                        last_message,
                    )
                ]
                if relevant_messages:
                    self._relevant_messages[self._keyword] += relevant_messages
                    self._relevant_keyword_calls.append(_get_keyword_call_path(keyword))

    def end_keyword(self, keyword: Keyword):  # noqa: ARG002
        if self._keyword and self._keyword_path not in _get_keyword_call_path(keyword):
            self._keyword = None

    def start_message(self, msg: Message):
        if self.report_configuration or self.basic_configuration:
            last_message = _get_last_message(self._relevant_messages[self._keyword])
            if _message_content_is_relevant(
                msg.message,
                self.report_configuration,
                self.basic_configuration,
                last_message,
            ):
                self._relevant_messages[self._keyword].append(msg)
                self._relevant_keyword_calls.append(_get_keyword_call_path(msg.parent))
            if _message_status_is_relevant(
                msg.level, self.report_configuration.message_status + self.basic_configuration.message_status
            ):
                self._relevant_messages[self._keyword].append(msg)
                self._relevant_keyword_calls.append(_get_keyword_call_path(msg.parent))

    def end_message(self, msg: Message):
        pass


def _get_all_submessages(keywords__, submessages_):
    for keyword in keywords__:
        if not isinstance(keyword, Keyword):
            continue
        submessages_ += list(keyword.messages)
        if keyword.body:
            _get_all_submessages(keyword.body, submessages_)
    return submessages_


def _get_last_message(messages):
    if messages:
        return messages[-1].message
    return ""


def _keyword_name_for_structure_is_relevant(keyword_name: str, accepted_names: list) -> bool:
    for accepted_name in accepted_names:
        pattern = f"^{accepted_name}"
        if regex.findall(pattern, keyword_name, regex.I):
            return True
    return False


def _check_name_relevance(keyword_name, keywords) -> list:
    return list(filter(lambda k: k.name is None or k.name.lower() == keyword_name.lower(), keywords))


def _get_keyword_call_path(keyword):
    # first instance needs to be a keyword not a warn or error of report summary
    if not isinstance(keyword, Keyword):
        return ""
    path = [keyword.kwname]
    k = keyword
    while k.parent:
        k = k.parent
        if isinstance(k, Keyword):
            path.append(k.kwname)
        if isinstance(k, TestCase):
            path.append(k.name)
            break

    keyword_path = ".".join(reversed(path))
    return keyword_path  # noqa: RET504


def _check_path_relevance(keyword, keywords):
    """returns keywords which
    - path is a part of given keyword path or
    - path is None"""
    keyword_path = _get_keyword_call_path(keyword)
    return [k for k in keywords if k.path is None or k.path.lower() in keyword_path.lower()]


def _check_index_relevance(call_index, keywords):
    return list(filter(lambda k: k.index is None or call_index in k.index, keywords))


def _keyword_name_as_info_is_relevant(keyword, report_configuration, basic_configuration):
    keyword_path = _get_keyword_call_path(keyword)
    for name_as_info in report_configuration.names_as_info + basic_configuration.names_as_info:
        pattern = f"{name_as_info}$"
        if regex.findall(pattern, keyword_path, regex.I):
            return True
    return False


def _all_keyword_messages_are_relevant(keyword, call_index, report_messages, report_configuration, basic_configuration):
    same_name_keywords = _check_name_relevance(
        keyword.kwname,
        report_configuration.keywords + basic_configuration.keywords,
    )
    if not same_name_keywords:
        return False

    same_path_keywords = _check_path_relevance(keyword, same_name_keywords)
    if not same_path_keywords:
        return False

    same_index_keywords = _check_index_relevance(call_index, same_path_keywords)
    if not same_index_keywords:
        return False

    if True in [k.set for k in same_index_keywords] and keyword.messages[0].message in [
        m.message for m in report_messages
    ]:
        return False

    return True


def _message_shall_be_ignored(message, report_configuration, basic_configuration, last_message):
    if message == last_message:  # same messages next to each other are never needed
        return True

    for ignored_message in report_configuration.ignored_messages + basic_configuration.ignored_messages:
        if ignored_message.lower() in message.lower():
            return True

    for pattern in report_configuration.ignored_message_pattern + basic_configuration.ignored_message_pattern:
        if regex.findall(pattern, message, regex.I + regex.DOTALL):
            return True
    return False


def _message_content_is_relevant(message, report_configuration, basic_configuration, last_message):
    if _message_shall_be_ignored(message, report_configuration, basic_configuration, last_message):
        return False

    for pattern in report_configuration.message_pattern + basic_configuration.message_pattern:
        if regex.findall(pattern, message, regex.I + regex.DOTALL):
            return True

    for text in report_configuration.message_text + basic_configuration.message_text:
        if text.lower() in message.lower():
            return True
    return False


def _message_status_is_relevant(message_level: str, relevant_levels: list):
    """checks if message is relevant due to his status

    Args:
        message_level (str): Level of the message to be checked
        relevant_levels (lsit): List with accepted levels
    """
    return message_level.lower() in [r.lower() for r in relevant_levels]
