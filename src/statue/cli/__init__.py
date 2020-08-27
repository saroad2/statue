"""CLI definitions."""
from statue.cli.cli import statue
from statue.cli.commands import commands_cli
from statue.cli.contexts import context_cli
from statue.cli.run import run_cli

__all__ = ["statue", "commands_cli", "context_cli", "run_cli"]
