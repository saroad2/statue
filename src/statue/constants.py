"""Constants module."""
from pathlib import Path

DESCRIPTION = """
Statue is a static code analysis tool combining all the tools you love in one place.
"""
DEFAULT_COMMANDS_FILE = Path(__file__).parent / "resources" / "commands.toml"

HELP = "help"
ARGS = "args"
CLEAR_ARGS = "clear_args"
ADD_ARGS = "add_args"
STANDARD = "standard"
