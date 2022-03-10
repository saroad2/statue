from statue.command import Command
from tests.constants import COMMAND1


def test_simple_command_init():
    command = Command(name=COMMAND1)
    assert command.name == COMMAND1
    assert command.args == []


def test_command_init_with_args():
    args = ["a", "b", "c", "D"]
    command = Command(name=COMMAND1, args=args)
    assert command.name == COMMAND1
    assert command.args == args
