"""CLI definitions."""
from statue.cli.cli import statue
from statue.cli.commands import command
from statue.cli.contexts import contexts
from statue.cli.run import run

__all__ = ["statue", "command", "list_commands", "contexts", "run"]
