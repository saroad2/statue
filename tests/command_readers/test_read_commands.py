# import pytest
#
# from statue.command import Command
# from statue.configuration import Configuration
# from statue.excptions import UnknownContext
# from tests.constants import (
#     ARG1,
#     ARG2,
#     ARG3,
#     ARG4,
#     ARG5,
#     COMMAND1,
#     COMMAND2,
#     COMMAND3,
#     COMMAND4,
#     COMMAND5,
#     COMMAND_HELP_STRING1,
#     COMMAND_HELP_STRING2,
#     COMMAND_HELP_STRING3,
#     COMMAND_HELP_STRING4,
#     COMMAND_HELP_STRING5,
#     CONTEXT1,
#     CONTEXT2,
#     CONTEXT3,
#     CONTEXT4,
#     NOT_EXISTING_CONTEXT,
# )
#
#
# def test_read_commands_with_empty_settings(empty_settings):
#     commands = Configuration.read_commands()
#     assert commands == []
#
#
# def test_read_commands_with_one_command_without_args(one_command_without_args_setting):
#     commands = Configuration.read_commands()
#     assert commands == [Command(name=COMMAND1, help=COMMAND_HELP_STRING1)]
#
#
# def test_read_commands_with_one_command_with_args(one_command_with_args_settings):
#     commands = Configuration.read_commands()
#     assert commands == [
#         Command(name=COMMAND1, help=COMMAND_HELP_STRING1, args=[ARG1, ARG2])
#     ]
#
#
# def test_read_commands_with_multiple_commands(
#     full_commands_settings_with_boolean_contexts,
# ):
#     commands = Configuration.read_commands()
#     assert commands == [
#         Command(name=COMMAND1, help=COMMAND_HELP_STRING1, args=[ARG1, ARG2]),
#         Command(name=COMMAND2, help=COMMAND_HELP_STRING2, args=[ARG3]),
#         Command(name=COMMAND3, help=COMMAND_HELP_STRING3),
#         Command(name=COMMAND4, help=COMMAND_HELP_STRING4, args=[ARG4, ARG5]),
#     ]
#
#
# def test_read_commands_with_non_passing_context(
#     full_commands_settings_with_boolean_contexts,
# ):
#     with pytest.raises(
#         UnknownContext,
#         match=f'^Could not find context named "{NOT_EXISTING_CONTEXT}".$',
#     ):
#         Configuration.read_commands(contexts=[NOT_EXISTING_CONTEXT])
#
#
# def test_read_commands_with_one_passing_context(
#     full_commands_settings_with_boolean_contexts,
# ):
#     commands = Configuration.read_commands(contexts=[CONTEXT3])
#     assert commands == [Command(name=COMMAND3, help=COMMAND_HELP_STRING3)]
#
#
# def test_read_commands_with_two_passing_context(
#     full_commands_settings_with_boolean_contexts,
# ):
#     commands = Configuration.read_commands(contexts=[CONTEXT2])
#     assert commands == [
#         Command(name=COMMAND1, help=COMMAND_HELP_STRING1, args=[ARG1, ARG2]),
#         Command(name=COMMAND2, help=COMMAND_HELP_STRING2, args=[ARG3]),
#     ]
#
#
# def test_read_commands_with_two_contexts(full_commands_settings_with_boolean_contexts):
#     commands = Configuration.read_commands(contexts=[CONTEXT1, CONTEXT2])
#     assert commands == [
#         Command(name=COMMAND1, help=COMMAND_HELP_STRING1, args=[ARG1, ARG2]),
#     ]
#
#
# def test_read_commands_with_non_standard_command(
#     full_commands_settings_with_boolean_contexts,
# ):
#     commands = Configuration.read_commands(contexts=[CONTEXT4])
#     assert commands == [
#         Command(name=COMMAND5, help=COMMAND_HELP_STRING5),
#     ]
#
#
# def test_read_commands_with_overrides_without_contexts(
#     full_commands_settings,
# ):
#     commands = Configuration.read_commands()
#     assert commands == [
#         Command(name=COMMAND1, help=COMMAND_HELP_STRING1, args=[ARG1, ARG2]),
#         Command(name=COMMAND3, help=COMMAND_HELP_STRING3, args=[]),
#     ]
#
#
# def test_read_commands_with_overrides_with_context(
#     full_commands_settings,
# ):
#     commands = Configuration.read_commands(contexts=[CONTEXT1])
#     assert commands == [
#         Command(name=COMMAND1, help=COMMAND_HELP_STRING1, args=[ARG3]),
#     ]
#
#
# def test_read_commands_with_overrides_with_another_context(
#     full_commands_settings,
# ):
#     commands = Configuration.read_commands(contexts=[CONTEXT2])
#     assert commands == [
#         Command(name=COMMAND1, help=COMMAND_HELP_STRING1, args=[ARG4, ARG5]),
#         Command(
#             name=COMMAND2,
#             help=COMMAND_HELP_STRING2,
#             args=[ARG3, ARG5],
#         ),
#     ]
#
#
# def test_read_commands_with_overrides_with_clear_args_context(
#     full_commands_settings,
# ):
#     commands = Configuration.read_commands(contexts=[CONTEXT3])
#     assert commands == [
#         Command(name=COMMAND1, help=COMMAND_HELP_STRING1, args=[]),
#     ]
#
#
# def test_read_commands_with_overrides_with_add_args_context(
#     full_commands_settings,
# ):
#     commands = Configuration.read_commands(contexts=[CONTEXT4])
#     assert commands == [
#         Command(name=COMMAND1, help=COMMAND_HELP_STRING1, args=[ARG1, ARG2, ARG5]),
#         Command(name=COMMAND2, help=COMMAND_HELP_STRING2, args=[]),
#     ]
#
#
# def test_read_commands_twice_with_overrides_with_add_args_context(
#     full_commands_settings,
# ):
#     commands1 = Configuration.read_commands(contexts=[CONTEXT4])
#     assert commands1 == [
#         Command(name=COMMAND1, help=COMMAND_HELP_STRING1, args=[ARG1, ARG2, ARG5]),
#         Command(name=COMMAND2, help=COMMAND_HELP_STRING2, args=[]),
#     ]
#     commands2 = Configuration.read_commands()
#     assert commands2 == [
#         Command(name=COMMAND1, help=COMMAND_HELP_STRING1, args=[ARG1, ARG2]),
#         Command(name=COMMAND3, help=COMMAND_HELP_STRING3, args=[]),
#     ]
#
#
# def test_read_commands_with_empty_allow_list(
#     full_commands_settings_with_boolean_contexts,
# ):
#     commands = Configuration.read_commands(allow_list=[])
#     assert commands == [
#         Command(name=COMMAND1, help=COMMAND_HELP_STRING1, args=[ARG1, ARG2]),
#         Command(name=COMMAND2, help=COMMAND_HELP_STRING2, args=[ARG3]),
#         Command(name=COMMAND3, help=COMMAND_HELP_STRING3),
#         Command(name=COMMAND4, help=COMMAND_HELP_STRING4, args=[ARG4, ARG5]),
#     ]
#
#
# def test_read_commands_with_non_empty_allow_list(
#     full_commands_settings_with_boolean_contexts,
# ):
#     commands = Configuration.read_commands(allow_list=[COMMAND1, COMMAND3])
#     assert commands == [
#         Command(
#             name=COMMAND1,
#             help=COMMAND_HELP_STRING1,
#             args=[ARG1, ARG2],
#         ),
#         Command(name=COMMAND3, help=COMMAND_HELP_STRING3, args=[]),
#     ]
#
#
# def test_read_commands_with_deny_list(full_commands_settings_with_boolean_contexts):
#     commands = Configuration.read_commands(deny_list=[COMMAND1, COMMAND3])
#     assert commands == [
#         Command(
#             name=COMMAND2,
#             help=COMMAND_HELP_STRING2,
#             args=[ARG3],
#         ),
#         Command(name=COMMAND4, help=COMMAND_HELP_STRING4, args=[ARG4, ARG5]),
#     ]
#
#
# def test_read_commands_with_no_context_in_context_inheritance(
#     commands_settings_with_context_inheritance,
# ):
#     commands = Configuration.read_commands(contexts=[])
#     assert commands == [
#         Command(name=COMMAND1, help=COMMAND_HELP_STRING1, args=[ARG1, ARG2]),
#         Command(name=COMMAND3, help=COMMAND_HELP_STRING3, args=[]),
#     ], "Commands are different than expected."
#
#
# def test_read_commands_with_root_context(commands_settings_with_context_inheritance):
#     commands = Configuration.read_commands(contexts=[CONTEXT3])
#     assert commands == [
#         Command(name=COMMAND1, help=COMMAND_HELP_STRING1, args=[]),
#         Command(name=COMMAND3, help=COMMAND_HELP_STRING3, args=[]),
#     ], "Commands are different than expected."
#
#
# def test_read_commands_with_override_context(
#     commands_settings_with_context_inheritance,
# ):
#     commands = Configuration.read_commands(contexts=[CONTEXT2])
#     assert commands == [
#         Command(name=COMMAND1, help=COMMAND_HELP_STRING1, args=[ARG4, ARG5]),
#         Command(name=COMMAND2, help=COMMAND_HELP_STRING2, args=[ARG3, ARG5]),
#     ], "Commands are different than expected."
#
#
# def test_read_commands_with_double_inheritance_context(
#     commands_settings_with_context_inheritance,
# ):
#     commands = Configuration.read_commands(contexts=[CONTEXT4])
#     assert commands == [
#         Command(name=COMMAND1, help=COMMAND_HELP_STRING1, args=[ARG1, ARG2, ARG5]),
#         Command(name=COMMAND2, help=COMMAND_HELP_STRING2, args=[]),
#         Command(name=COMMAND3, help=COMMAND_HELP_STRING3, args=[]),
#     ], "Commands are different than expected."
