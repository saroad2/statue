"""Configuration related CLIs."""
from statue.cli.config.config_cli import config_cli
from statue.cli.config.config_commands import (
    add_command_cli,
    edit_command_cli,
    fixate_commands_versions_cli,
    remove_command_cli,
)
from statue.cli.config.config_contexts import (
    add_context_cli,
    edit_context_cli,
    remove_context_cli,
)
from statue.cli.config.config_general import set_history_size_cli, set_mode_cli
from statue.cli.config.config_init import init_config_cli
from statue.cli.config.config_show import show_config_cli
from statue.cli.config.config_sources import (
    add_source_to_configuration_cli,
    edit_source_in_configuration_cli,
    remove_source_from_configuration_cli,
)
from statue.cli.show_tree import show_tree_cli

__all__ = [
    "config_cli",
    "set_mode_cli",
    "set_history_size_cli",
    "add_context_cli",
    "edit_context_cli",
    "remove_context_cli",
    "add_command_cli",
    "edit_command_cli",
    "remove_command_cli",
    "fixate_commands_versions_cli",
    "add_source_to_configuration_cli",
    "edit_source_in_configuration_cli",
    "remove_source_from_configuration_cli",
    "init_config_cli",
    "show_config_cli",
    "show_tree_cli",
]
