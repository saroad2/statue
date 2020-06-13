"""Constants module."""
from pathlib import Path

DESCRIPTION = """
Eddington Static is a static analysis tool used by the Eddington platform repositories.
"""
DEFAULT_COMMANDS_FILE = Path(__file__).parent / "resources" / "commands.toml"

HELP = "help"
ARGS = "args"
CLEAR_ARGS = "clear_args"
ADD_ARGS = "add_args"
STANDARD = "standard"
