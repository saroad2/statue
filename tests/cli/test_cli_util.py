from statue.cli.util import install_commands_if_missing
from tests.constants import COMMAND1, COMMAND2, COMMAND3
from tests.util import command_mock


def test_install_commands_when_all_installed():
    commands = [command_mock(COMMAND1), command_mock(COMMAND2), command_mock(COMMAND3)]
    install_commands_if_missing(commands)
    for command in commands:
        command.install.assert_not_called()


def test_install_commands_when_is_not_installed():
    commands = [
        command_mock(COMMAND1),
        command_mock(COMMAND2, installed=False),
        command_mock(COMMAND3),
    ]
    install_commands_if_missing(commands)
    commands[0].install.assert_not_called()
    commands[1].install.assert_called()
    commands[2].install.assert_not_called()


def test_install_commands_with_same_command_twice():
    commands = [
        command_mock(COMMAND2, installed=False),
        command_mock(COMMAND2, installed=False),
    ]
    install_commands_if_missing(commands)
    commands[0].install.assert_called()
    commands[1].install.assert_not_called()
