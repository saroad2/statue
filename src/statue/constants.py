"""Constants module."""
from pathlib import Path

DEFAULT_COMMANDS_FILE = Path(__file__).parent / "resources" / "commands.toml"

HELP = "help"
ARGS = "args"
CLEAR_ARGS = "clear_args"
ADD_ARGS = "add_args"
STANDARD = "standard"
CONTEXTS = "contexts"
ALLOW_LIST = "allow_list"
DENY_LIST = "deny_list"
COMMANDS = "commands"
SOURCES = "sources"
