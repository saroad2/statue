import mock

from statue.config.configuration import Configuration


def test_configuration_to_toml():
    configuration = Configuration()
    configuration.as_dict = mock.Mock()
    path = mock.MagicMock()
    path_fd = path.open.return_value.__enter__.return_value

    with mock.patch("tomli_w.dump") as dump_mock:
        configuration.to_toml(path)
        dump_mock.assert_called_once_with(configuration.as_dict.return_value, path_fd)
        path.open.assert_called_once_with(mode="wb")
