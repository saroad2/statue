from statue.config.configuration import Configuration


def test_configuration_default_configuration_path(tmp_path, mock_cwd):

    assert Configuration.configuration_path() == mock_cwd / "statue.toml"


def test_configuration_configuration_path(tmp_path):

    assert Configuration.configuration_path(tmp_path) == tmp_path / "statue.toml"


def test_configuration_cache_path(tmp_path):

    assert Configuration.cache_path(tmp_path) == tmp_path / ".statue"
