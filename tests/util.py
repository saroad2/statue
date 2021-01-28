from unittest import mock

from statue.command import Command


def build_contexts_map(*contexts):
    return {context.name: context for context in contexts}


def command_mock(name, installed=True, return_code=None):
    command = Command(name=name, help="This is help")
    command.name = name
    command.installed = mock.Mock(return_value=installed)
    command.install = mock.Mock()
    if return_code is not None:
        command.execute = mock.Mock(return_value=return_code)
    return command


def assert_calls(mock_obj, calls):
    assert mock_obj.call_count == len(
        calls
    ), f"Expected {len(calls)} calls, got {mock_obj.call_count}"
    for i, expected_call in enumerate(calls):
        actual_call = mock_obj.call_args_list[i]
        assert (
            actual_call == expected_call
        ), f"Call {i} is different than expected. {actual_call} != {expected_call}"
