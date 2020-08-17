from pytest_cases import parametrize_with_cases, THIS_MODULE

from statue.command import Command
from statue.verbosity import SILENT, VERBOSE

INPUT_PATH = "input_path"


def case_no_args():
    name = "command1"
    help_string = "help1"
    inp = Command(name=name, help=help_string)
    output = dict(
        name=name,
        help=help_string,
        args=[],
        command_input=[name, INPUT_PATH],
        print=f'Running the following command: "{name} {INPUT_PATH}"',
        repr=f"Command(name='{name}', help='{help_string}', args=[])",
    )
    return inp, output


def case_one_arg():
    name = "command2"
    arg1 = "arg1"
    help_string = "help2"
    inp = Command(name=name, help=help_string, args=[arg1])
    output = dict(
        name=name,
        help=help_string,
        args=[arg1],
        command_input=[name, INPUT_PATH, arg1],
        print=f'Running the following command: "{name} {INPUT_PATH} {arg1}"',
        repr=f"Command(name='{name}', help='{help_string}', args=['{arg1}'])",
    )
    return inp, output


def case_two_args():
    name = "command3"
    help_string = "help3"
    arg1 = "arg1"
    arg2 = "arg2"
    inp = Command(name=name, help=help_string, args=[arg1, arg2])
    output = dict(
        name=name,
        help=help_string,
        args=[arg1, arg2],
        command_input=[name, INPUT_PATH, arg1, arg2],
        print=(
            "Running the following command: " f'"{name} {INPUT_PATH} {arg1} {arg2}"'
        ),
        repr=f"Command(name='{name}', help='{help_string}', args=['{arg1}', '{arg2}'])",
    )
    return inp, output


@parametrize_with_cases(argnames="command, out", cases=THIS_MODULE)
def test_name_is_set(command, out):
    assert command.name == out["name"]


@parametrize_with_cases(argnames="command, out", cases=THIS_MODULE)
def test_help_is_set(command, out):
    assert command.help == out["help"]


@parametrize_with_cases(argnames="command, out", cases=THIS_MODULE)
def test_args_are_set(command, out):
    assert command.args == out["args"]


@parametrize_with_cases(argnames="command, out", cases=THIS_MODULE)
def test_execute(command, out, subprocess_mock, environ):
    command.execute(INPUT_PATH)
    subprocess_mock.assert_called_with(
        out["command_input"], env=environ, check=False, capture_output=False
    )


@parametrize_with_cases(argnames="command, out", cases=THIS_MODULE)
def test_execute_silently(command, out, subprocess_mock, environ):
    command.execute(INPUT_PATH, verbosity=SILENT)
    subprocess_mock.assert_called_with(
        out["command_input"], env=environ, check=False, capture_output=True
    )


@parametrize_with_cases(argnames="command, out", cases=THIS_MODULE)
def test_execute_verbosely(command, out, subprocess_mock, environ, print_mock):
    command.execute(INPUT_PATH, verbosity=VERBOSE)
    subprocess_mock.assert_called_with(
        out["command_input"], env=environ, check=False, capture_output=False
    )
    print_mock.assert_called_with(out["print"])


@parametrize_with_cases(argnames="command, out", cases=THIS_MODULE)
def test_representation_string(command, out):
    assert str(command) == out["repr"]


def test_command_equals():
    name = "command1"
    help_string = "help1"
    args = ["arg1", "arg2", "arg3"]
    command1 = Command(name=name, help=help_string, args=args)
    command2 = Command(name=name, help=help_string, args=args)
    assert command1 == command2
    assert not command1 != command2  # pylint: disable=C0113


def test_command_not_equals_because_of_different_names():
    name1 = "command1"
    name2 = "command2"
    help_string = "help1"
    args = ["arg1", "arg2", "arg3"]
    command1 = Command(name=name1, help=help_string, args=args)
    command2 = Command(name=name2, help=help_string, args=args)
    assert not command1 == command2  # pylint: disable=C0113
    assert command1 != command2


def test_command_not_equals_because_of_different_helps():
    name = "command1"
    help_string1 = "help1"
    help_string2 = "help2"
    args = ["arg1", "arg2", "arg3"]
    command1 = Command(name=name, help=help_string1, args=args)
    command2 = Command(name=name, help=help_string2, args=args)
    assert not command1 == command2  # pylint: disable=C0113
    assert command1 != command2


def test_command_not_equals_because_of_different_args():
    name = "command1"
    help_string = "help1"
    args1 = ["arg1", "arg2", "arg3"]
    args2 = ["arg4", "arg5"]
    command1 = Command(name=name, help=help_string, args=args1)
    command2 = Command(name=name, help=help_string, args=args2)
    assert not command1 == command2  # pylint: disable=C0113
    assert command1 != command2
