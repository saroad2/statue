"""Get Statue global configuration."""
from copy import deepcopy
from pathlib import Path
from typing import Any, MutableMapping, Optional, List

import toml

from statue.constants import COMMANDS, CONTEXTS, DEFAULT_CONFIGURATION_FILE, SOURCES
from statue.excptions import EmptyConfiguration


class __ConfigurationMetaclass:

    __default_configuration: Optional[MutableMapping[str, Any]] = None
    __statue_configuration: Optional[MutableMapping[str, Any]] = None

    @property
    def default_configuration(self) -> Optional[MutableMapping[str, Any]]:
        if self.__default_configuration is None:
            self.__load_default_configuration()
        return deepcopy(self.__default_configuration)

    @default_configuration.setter
    def default_configuration(self, default_configuration) -> None:
        self.__default_configuration = default_configuration

    @property
    def statue_configuration(self) -> Optional[MutableMapping[str, Any]]:
        if self.__statue_configuration is not None:
            return deepcopy(self.__statue_configuration)
        if self.default_configuration is not None:
            return self.default_configuration
        raise EmptyConfiguration()

    @statue_configuration.setter
    def statue_configuration(self, statue_configuration) -> None:
        self.__statue_configuration = statue_configuration

    @property
    def commands_configuration(self) -> Optional[MutableMapping[str, Any]]:
        return self.statue_configuration.get(COMMANDS, None)

    @property
    def sources_configuration(self) -> Optional[MutableMapping[str, Any]]:
        return self.statue_configuration.get(SOURCES, None)

    @property
    def commands_names_list(self) -> List[str]:
        if self.commands_configuration is None:
            return []
        return list(self.commands_configuration.keys())

    @property
    def contexts_configuration(self) -> Optional[MutableMapping[str, Any]]:
        return self.statue_configuration.get(CONTEXTS, None)

    def __load_default_configuration(self):
        self.__default_configuration = toml.load(DEFAULT_CONFIGURATION_FILE)

    def load_configuration(self, statue_configuration_path: Path,) -> None:
        """
        Get statue configuration.

        This method combines default configuration with user-defined configuration, read
        from configuration file.

        :param statue_configuration_path: User-defined file path containing
        repository-specific configurations
        :returns: a configuration dictionary object.
        """
        if not statue_configuration_path.exists():
            return None
        statue_config = toml.load(statue_configuration_path)
        if self.default_configuration is not None:
            statue_config[COMMANDS] = self.default_configuration.get(COMMANDS, {})
            statue_config[CONTEXTS] = self.default_configuration.get(CONTEXTS, {})
        self.statue_configuration = statue_config

    def reset_configuration(self):
        self.statue_configuration = None


Configuration = __ConfigurationMetaclass()
