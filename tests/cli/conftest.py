from pathlib import Path

import pytest
import toml
from click.testing import CliRunner

from statue.constants import OVERRIDE, STATUE


@pytest.fixture
def cli_runner():
    return CliRunner()


@pytest.fixture
def dummy_cwd(mocker, tmpdir):
    cwd = mocker.patch.object(Path, "cwd")
    cwd.return_value = tmpdir
    return Path(tmpdir)


@pytest.fixture
def empty_configuration(dummy_cwd, clear_configuration):
    configuration = {
        STATUE: {OVERRIDE: True},
    }
    with open(dummy_cwd / "statue.toml", mode="w") as configuration_file:
        toml.dump(configuration, configuration_file)
    return configuration
