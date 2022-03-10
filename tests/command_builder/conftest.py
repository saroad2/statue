import pytest

from statue.command_builder import CommandBuilder


@pytest.fixture
def mock_get_package(mocker):
    return mocker.patch.object(CommandBuilder, "_get_package")
