"""Get Statue global configuration."""
from copy import deepcopy
from pathlib import Path
from typing import Any, List, MutableMapping, Optional

import toml

from statue.constants import COMMANDS, CONTEXTS, DEFAULT_CONFIGURATION_FILE, SOURCES
from statue.excptions import EmptyConfiguration

__all__ = ["Configuration"]


class __ConfigurationMetaclass:  # pylint: disable=invalid-name

    __default_configuration: Optional[MutableMapping[str, Any]] = None
    __statue_configuration: Optional[MutableMapping[str, Any]] = None

    @property
    def default_configuration(self) -> Optional[MutableMapping[str, Any]]:
        """Getter of default configuration."""
        if self.__default_configuration is None:
            self.__load_default_configuration()
        return deepcopy(self.__default_configuration)

    @default_configuration.setter
    def default_configuration(
        self, default_configuration: Optional[MutableMapping[str, Any]]
    ) -> None:
        """Setter of default configuration."""
        self.__default_configuration = default_configuration

    @property
    def statue_configuration(self) -> MutableMapping[str, Any]:
        """Getter of general statue configuration."""
        if self.__statue_configuration is not None:
            return deepcopy(self.__statue_configuration)
        if self.default_configuration is not None:
            return self.default_configuration
        raise EmptyConfiguration()

    @statue_configuration.setter
    def statue_configuration(
        self, statue_configuration: Optional[MutableMapping[str, Any]]
    ) -> None:
        """Setter of general statue configuration."""
        self.__statue_configuration = statue_configuration

    @property
    def commands_configuration(self) -> Optional[MutableMapping[str, Any]]:
        """Getter of the commands configuration."""
        return self.statue_configuration.get(COMMANDS, None)

    @property
    def commands_names_list(self) -> List[str]:
        """Getter of the commands list."""
        if self.commands_configuration is None:
            return []
        return list(self.commands_configuration.keys())

    @property
    def sources_configuration(self) -> Optional[MutableMapping[str, Any]]:
        """Getter of the sources configuration."""
        return self.statue_configuration.get(SOURCES, None)

    @property
    def contexts_configuration(self) -> Optional[MutableMapping[str, Any]]:
        """Getter of the contexts configuration."""
        return self.statue_configuration.get(CONTEXTS, None)

    def __load_default_configuration(self) -> None:
        self.__default_configuration = toml.load(DEFAULT_CONFIGURATION_FILE)

    def load_configuration(self, statue_configuration_path: Path,) -> None:
        """
        load statue configuration.

        This method combines default configuration with user-defined configuration, read
        from configuration file.

        :param statue_configuration_path: User-defined file path containing
        repository-specific configurations
        """
        if not statue_configuration_path.exists():
            return
        statue_config = toml.load(statue_configuration_path)
        if self.default_configuration is not None:
            statue_config[COMMANDS] = self.default_configuration.get(COMMANDS, {})
            statue_config[CONTEXTS] = self.default_configuration.get(CONTEXTS, {})
        self.statue_configuration = statue_config

    def reset_configuration(self) -> None:
        """Reset the general statue configuration."""
        self.statue_configuration = None  # type:ignore


Configuration = __ConfigurationMetaclass()
