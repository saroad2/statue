from pathlib import Path

import pytest
import toml
from click.testing import CliRunner

from statue.constants import OVERRIDE, STATUE


@pytest.fixture
def cli_runner():
    return CliRunner()
