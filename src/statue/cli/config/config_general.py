"""General configuration CLI."""
import click

from statue.cli.common_flags import config_path_option
from statue.cli.config.config_cli import config_cli
from statue.config.configuration_builder import ConfigurationBuilder
from statue.runner import RunnerMode


@config_cli.command("set-mode")
@config_path_option
@click.argument(
    "mode",
    type=click.Choice([mode.name.lower() for mode in RunnerMode], case_sensitive=False),
    callback=lambda ctx, param, value: (None if value is None else value.upper()),
)
def set_mode_cli(mode, config):
    """Choose which runner mode will be used by default."""
    if config is None:
        config = ConfigurationBuilder.configuration_path()
    configuration = ConfigurationBuilder.build_configuration_from_file(config)
    configuration.default_mode = RunnerMode[mode]
    configuration.to_toml(config)
    click.echo("Mode successfully set!")
