"""General configuration CLI."""
import click

from statue.cli.common_flags import config_path_option
from statue.cli.config.config_cli import config_cli
from statue.config.configuration import Configuration
from statue.runner import RunnerMode


@config_cli.command("set-mode")
@click.argument(
    "mode",
    type=click.Choice([mode.name.lower() for mode in RunnerMode], case_sensitive=False),
    callback=lambda ctx, param, value: (None if value is None else value.upper()),
)
@config_path_option
def set_mode_cli(mode, config):
    """Choose which runner mode will be used by default."""
    if config is None:
        config = Configuration.configuration_path()
    configuration = Configuration.from_file(config)
    configuration.default_mode = RunnerMode[mode]
    configuration.to_toml(config)
    click.echo("Mode was successfully set!")


@config_cli.command("set-history-size")
@click.argument("size", type=int, nargs=1)
@config_path_option
def set_history_size_cli(size, config):
    """Choose which runner mode will be used by default."""
    if config is None:
        config = Configuration.configuration_path()
    configuration = Configuration.from_file(config)
    configuration.cache.history_size = size
    configuration.to_toml(config)
    click.echo("History size was successfully set!")


@config_cli.command("enable-cache")
@config_path_option
def enable_cache_cli(config):
    """Enabled caching in configuration."""
    if config is None:
        config = Configuration.configuration_path()
    configuration = Configuration.from_file(config)
    configuration.cache.enabled = True
    configuration.to_toml(config)
    click.echo("Caching is enabled!")


@config_cli.command("disable-cache")
@config_path_option
def disable_cache_cli(config):
    """Disabled caching in configuration."""
    if config is None:
        config = Configuration.configuration_path()
    configuration = Configuration.from_file(config)
    configuration.cache.enabled = False
    configuration.to_toml(config)
    click.echo("Caching is disabled!")
