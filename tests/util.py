from unittest.mock import Mock


def command_mock(name, installed=True, return_code=None):
    mock = Mock()
    mock.name = name
    mock.installed.return_value = installed
    if return_code is not None:
        mock.execute.return_value = return_code
    return mock
