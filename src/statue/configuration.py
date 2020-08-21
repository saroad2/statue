"""Get Statue global configuration."""
from pathlib import Path
from typing import Any, MutableMapping, Optional

import toml

from statue.constants import COMMANDS, DEFAULT_CONFIGURATION_FILE


def get_configuration(
    statue_configuration_path: Path,
    default_configuration_path: Path = DEFAULT_CONFIGURATION_FILE,
) -> Optional[MutableMapping[str, Any]]:
    """
    Get statue configuration.

    This method combines default configuration with user-defined configuration, read
    from configuration file.

    :param statue_configuration_path: User-defined file path containing
    repository-specific configurations
    :param default_configuration_path: Path to default file. can be defined by the
    user or default file.
    :returns: a configuration dictionary object.
    """
    if not statue_configuration_path.exists():
        return None
    statue_config = toml.load(statue_configuration_path)
    default_configuration: MutableMapping[str, Any] = {}
    if default_configuration_path.exists():
        default_configuration = toml.load(default_configuration_path)
    statue_config[COMMANDS] = default_configuration.get(COMMANDS, {})
    return statue_config
