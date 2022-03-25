"""Configuration main CLI."""


from statue.cli.cli import statue_cli


@statue_cli.group("config")
def config_cli():
    """Configuration related actions."""
