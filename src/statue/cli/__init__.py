"""CLI definitions."""
from statue.cli.cli import statue_cli
from statue.cli.commands import commands_cli
from statue.cli.config import config_cli
from statue.cli.contexts import context_cli
from statue.cli.history import history_cli
from statue.cli.run import run_cli

__all__ = [
    "statue_cli",
    "commands_cli",
    "config_cli",
    "context_cli",
    "run_cli",
    "history_cli",
]
