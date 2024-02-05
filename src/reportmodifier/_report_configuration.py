from pathlib import Path
import yaml


class ReportConfiguration:
    def __init__(self, path) -> None:
        self.__path = path
        self.__yaml_config = None
        self.__keywords = None
        self.__messages = None
        self.__ignored_messages = None
        self.__keyword_names_as_info = None
        self.__keyword_as_structure = None

    def __config(self):
        if self.__path is None:
            self.__yaml_config = dict()
            return self.__yaml_config
        assert Path(self.__path).exists(
        ) is True, f"Configuration path does not exist! {self.__path}"
        if self.__yaml_config is None:
            self.__yaml_config = yaml.safe_load(
                Path(self.__path).read_text(encoding='utf-8'))
        return self.__yaml_config

    @property
    def keyword_as_structure(self):
        if self.__keyword_as_structure is None:
            self.__keyword_as_structure = []
            keywords = self.__config().get('keyword_as_structure')
            if keywords is not None:
                self.__keyword_as_structure = [
                    KeywordAsStructure(c) for c in list(keywords)]
        return self.__keyword_as_structure

    @property
    def keywords(self):
        if self.__keywords is None:
            self.__keywords = []
            if self.__config().get('keywords') is not None:
                self.__keywords = [KeywordConfig(c) for c in list(
                    self.__config().get('keywords'))]
        return self.__keywords

    @property
    def keyword_names(self):
        return [k.name for k in self.keywords]

    def _message_configs(self):
        if self.__messages is None:
            self.__messages = list()
            if 'messages' in list(self.__config()):
                self.__messages = [MessageConfig(
                    c) for c in list(self.__config()['messages'])]
        return self.__messages

    @property
    def message_pattern(self):
        return list(set([k.pattern for k in self._message_configs() if k.pattern is not None]))

    @property
    def message_text(self):
        self.message_pattern
        return list(set([k.text for k in self._message_configs() if k.text is not None]))

    def _ignored_message_configs(self):
        if self.__ignored_messages is None:
            self.__ignored_messages = list()
            if 'ignored_messages' in list(self.__config()):
                self.__ignored_messages = [MessageConfig(
                    c) for c in list(self.__config()['ignored_messages'])]
        return self.__ignored_messages

    @property
    def ignored_message_pattern(self):
        return [k.pattern for k in self._ignored_message_configs() if k.pattern is not None]

    @property
    def ignored_messages(self):
        self.ignored_message_pattern
        return [c.text for c in self._ignored_message_configs() if c.text is not None]

    @property
    def names_as_info(self):
        if self.__keyword_names_as_info is None:
            self.__keyword_names_as_info = list()
            if 'keyword_name_as_info' in list(self.__config()):
                self.__keyword_names_as_info = [NameAsInfo(c) for c in list(
                    self.__config()['keyword_name_as_info'])]
        return [k.name for k in self.__keyword_names_as_info]


class KeywordConfig:
    def __init__(self, config) -> None:
        self.__config = config

    @property
    def name(self):
        if isinstance(self.__config, str):
            result = self.__config.split('[')[0].strip()
            if '.' not in result:
                return result.strip()
            else:
                return result.split('.')[-1]
        elif isinstance(self.__config, dict):
            return self.__config.get('name')

    @property
    def path(self):
        if isinstance(self.__config, dict):
            return self.__config.get('path')
        path = self.__config.split('[')[0].strip()
        path_parts = path.split('.')
        if len(path_parts) > 1:
            return path

    @property
    def index(self) -> list | None:
        if isinstance(self.__config, dict):
            i = self.__config.get('index')
            if i and not isinstance(i, list):
                i = [i]
            return i
        parts = self.__config.split('[')
        if len(parts) > 1:
            return [int(i) for i in parts[-1].replace(']', '').split(',')]

    @property
    def set(self):
        if isinstance(self.__config, dict):
            return self.__config.get('set')
        return False


class MessageConfig:
    def __init__(self, config) -> None:
        self.__config = config

    @property
    def pattern(self):
        if isinstance(self.__config, dict):
            return self.__config.get('pattern')
        return self.__config

    @property
    def text(self):
        if isinstance(self.__config, dict):
            return self.__config.get('text')


class NameAsInfo:
    def __init__(self, config) -> None:
        self.__config = config

    @property
    def name(self):
        if isinstance(self.__config, dict):
            return self.__config.get('name')
        return self.__config


class KeywordAsStructure:
    def __init__(self, config) -> None:
        self.__config = config

    @property
    def name(self):
        if isinstance(self.__config, dict):
            return self.__config.get('name')
        return self.__config
