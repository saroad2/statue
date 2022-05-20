"""Show configuration CLI."""
from pathlib import Path
from typing import Optional

import click

from statue.cli.common_flags import config_path_option
from statue.cli.config.config_cli import config_cli
from statue.config.configuration import Configuration
from statue.constants import ENCODING


@config_cli.command("show")
@config_path_option
def show_config_cli(config: Optional[Path]):
    """Show configuration file context."""
    if config is None:
        config = Configuration.configuration_path()
    with open(config, mode="r", encoding=ENCODING) as config_file:
        lines = config_file.readlines()
    click.echo_via_pager(lines)
