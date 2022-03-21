from statue.config.configuration_builder import ConfigurationBuilder


def test_configuration_builder_configuration_path(tmp_path):

    assert ConfigurationBuilder.configuration_path(tmp_path) == tmp_path / "statue.toml"


def test_configuration_builder_cache_path(tmp_path):

    assert ConfigurationBuilder.cache_path(tmp_path) == tmp_path / ".statue"
