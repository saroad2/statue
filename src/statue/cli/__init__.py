"""CLI definitions."""
from statue.cli.cli import statue
from statue.cli.commands import install_commands, list_commands
from statue.cli.contexts import contexts
from statue.cli.run import run

__all__ = ["statue", "install_commands", "list_commands", "contexts", "run"]
