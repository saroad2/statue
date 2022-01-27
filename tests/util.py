from unittest import mock

from statue.command import Command, CommandEvaluation
from statue.evaluation import Evaluation, SourceEvaluation


def build_contexts_map(*contexts):
    return {context.name: context for context in contexts}


def build_failure_evaluation(commands_map):
    return Evaluation(
        {
            source: SourceEvaluation(
                [
                    CommandEvaluation(command=command, success=False)
                    for command in commands
                ]
            )
            for source, commands in commands_map.items()
        }
    )


def command_mock(
    name, installed=True, version=None, success=True, installed_version="0.0.1"
):
    command = Command(name=name, help="This is help", version=version)
    command.name = name
    command.install = mock.Mock()
    command.update = mock.Mock()
    command.update_to_version = mock.Mock()
    get_package = mock.Mock()
    if not installed:
        get_package.return_value = None
    else:
        get_package.return_value.version = installed_version
    command._get_package = get_package  # pylint: disable=protected-access
    command_evaluation = CommandEvaluation(command=command, success=success)
    command.execute = mock.Mock(return_value=command_evaluation)
    return command


def evaluation_mock(successful_commands, total_commands):
    evaluation = mock.Mock()
    evaluation.successful_commands_number = successful_commands
    evaluation.commands_number = total_commands
    evaluation.success = successful_commands == total_commands
    return evaluation


def assert_calls(mock_obj, calls):
    assert mock_obj.call_count == len(
        calls
    ), f"Expected {len(calls)} calls, got {mock_obj.call_count}"
    for i, expected_call in enumerate(calls):
        actual_call = mock_obj.call_args_list[i]
        assert (
            actual_call == expected_call
        ), f"Call {i} is different than expected. {actual_call} != {expected_call}"
