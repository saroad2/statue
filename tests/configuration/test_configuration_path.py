from unittest import mock

from statue.configuration import Configuration


def test_configuration_path_in_directory_path():
    directory = mock.MagicMock()
    configuration_path = Configuration.configuration_path(directory)
    assert configuration_path == directory.__truediv__.return_value
    directory.__truediv__.assert_called_with("statue.toml")


def test_configuration_path_in_directory_string():
    directory_as_string = "/path/to/directory"
    directory = mock.MagicMock()
    with mock.patch("statue.configuration.Path") as mock_path:
        mock_path.return_value = directory
        configuration_path = Configuration.configuration_path(directory_as_string)
        mock_path.assert_called_once_with(directory_as_string)
    assert configuration_path == directory.__truediv__.return_value
    directory.__truediv__.assert_called_with("statue.toml")
