"""Constants module."""
from pathlib import Path

STATUE = "STATUE"
ENCODING = "utf-8"

HISTORY_SIZE = 30

DEFAULT_CONFIGURATION_FILE = Path(__file__).parent / "resources" / "defaults.toml"

HELP = "help"
ARGS = "args"
CLEAR_ARGS = "clear_args"
ADD_ARGS = "add_args"
STANDARD = "standard"
ALLOW_LIST = "allow_list"
DENY_LIST = "deny_list"
ALLOWED_CONTEXTS = "allowed_contexts"
REQUIRED_CONTEXTS = "required_contexts"
ALIASES = "aliases"
PARENT = "parent"
ALLOWED_BY_DEFAULT = "allowed_by_default"
IS_DEFAULT = "is_default"
VERSION = "version"

COMMANDS = "commands"
CONTEXTS = "contexts"
SOURCES = "sources"

OVERRIDE = "OVERRIDE"

DATETIME_FORMAT = "%m/%d/%Y, %H:%M:%S"
