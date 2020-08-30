"""Constants module."""
from pathlib import Path

STATUE = "STATUE"

DEFAULT_CONFIGURATION_FILE = Path(__file__).parent / "resources" / "defaults.toml"

HELP = "help"
ARGS = "args"
CLEAR_ARGS = "clear_args"
ADD_ARGS = "add_args"
STANDARD = "standard"
ALLOW_LIST = "allow_list"
DENY_LIST = "deny_list"
PARENT = "parent"

COMMANDS = "commands"
CONTEXTS = "contexts"
SOURCES = "sources"

OVERRIDE = "OVERRIDE"
