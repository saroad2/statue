import pytest

from statue.configuration import Configuration


@pytest.fixture
def clear_configuration():
    yield
    Configuration.reset_configuration()
