from statue.command import Command
from tests.constants import COMMAND1, COMMAND_HELP_STRING1


def test_simple_command_init():
    command = Command(name=COMMAND1, help=COMMAND_HELP_STRING1)
    assert command.name == COMMAND1
    assert command.help == COMMAND_HELP_STRING1
    assert command.args == []
    assert command.version is None


def test_command_init_with_args():
    args = ["a", "b", "c", "D"]
    command = Command(name=COMMAND1, help=COMMAND_HELP_STRING1, args=args)
    assert command.name == COMMAND1
    assert command.help == COMMAND_HELP_STRING1
    assert command.args == args
    assert command.version is None


def test_command_init_with_version():
    version = "1.5.2"
    command = Command(name=COMMAND1, help=COMMAND_HELP_STRING1, version=version)
    assert command.name == COMMAND1
    assert command.help == COMMAND_HELP_STRING1
    assert command.args == []
    assert command.version == version


def test_command_init_with_args_and_version():
    args = ["a", "b", "c", "D"]
    version = "1.5.2"
    command = Command(
        name=COMMAND1, help=COMMAND_HELP_STRING1, args=args, version=version
    )
    assert command.name == COMMAND1
    assert command.help == COMMAND_HELP_STRING1
    assert command.args == args
    assert command.version == version
