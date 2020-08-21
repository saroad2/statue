"""Get Statue global configuration."""
from pathlib import Path
from typing import Any, MutableMapping, Optional

import toml

from statue.constants import COMMANDS, DEFAULT_COMMANDS_FILE


def get_configuration(
    statue_configuration_path: Path,
    commands_configuration_path: Path = DEFAULT_COMMANDS_FILE,
) -> Optional[MutableMapping[str, Any]]:
    """
    Get statue configuration.

    :param statue_configuration_path: User-defined file path containing
    repository-specific configurations
    :param commands_configuration_path: Path to commands file. can be defined by the
    user or default file.
    :returns: a configuration dictionary object.
    """
    if not statue_configuration_path.exists():
        return None
    statue_config = toml.load(statue_configuration_path)
    if commands_configuration_path.exists():
        statue_config[COMMANDS] = toml.load(commands_configuration_path)
    return statue_config
