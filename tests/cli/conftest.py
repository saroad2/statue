import pytest
from click.testing import CliRunner

from statue.cache import Cache


@pytest.fixture
def cli_runner():
    return CliRunner()


# Cache Mocks


@pytest.fixture
def mock_cache_extract_time_stamp_from_path(mocker):
    return mocker.patch.object(Cache, "extract_time_stamp_from_path")
