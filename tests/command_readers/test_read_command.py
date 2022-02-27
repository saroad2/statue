import pytest
from pytest_cases import THIS_MODULE, case, parametrize_with_cases

from statue.command import Command
from statue.command_builder import CommandBuilder, ContextSpecification
from statue.configuration import Configuration
from statue.constants import COMMANDS
from statue.context import Context
from statue.exceptions import (
    InvalidCommand,
    MissingConfiguration,
    UnknownCommand,
    UnknownContext,
)
from tests.constants import (
    ARG1,
    ARG2,
    ARG3,
    ARG4,
    ARG5,
    COMMAND1,
    COMMAND2,
    COMMAND3,
    COMMAND_HELP_STRING1,
    COMMAND_HELP_STRING2,
    CONTEXT1,
    CONTEXT2,
    CONTEXT3,
    CONTEXT_HELP_STRING1,
    CONTEXT_HELP_STRING2,
    CONTEXT_HELP_STRING3,
    FAILED_TAG,
    NOT_EXISTING_CONTEXT,
    SUCCESSFUL_TAG,
)

# Success cases
from tests.util import build_commands_builders_map


@case(tags=[SUCCESSFUL_TAG])
def case_with_no_contexts(clear_configuration):
    configuration = {
        COMMANDS: build_commands_builders_map(
            CommandBuilder(
                name=COMMAND1,
                help=COMMAND_HELP_STRING1,
                default_args=[ARG1],
                contexts_specifications={
                    CONTEXT1: ContextSpecification(add_args=[ARG2, ARG3])
                },
            )
        ),
    }
    kwargs = dict(command_name=COMMAND1)
    command = Command(name=COMMAND1, args=[ARG1], help=COMMAND_HELP_STRING1)
    return configuration, kwargs, command


@case(tags=[SUCCESSFUL_TAG])
def case_with_allowed_context(clear_configuration):
    Configuration.contexts_repository.add_contexts(
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    )
    configuration = {
        COMMANDS: build_commands_builders_map(
            CommandBuilder(
                name=COMMAND1,
                help=COMMAND_HELP_STRING1,
                default_args=[ARG1],
                allowed_contexts=[CONTEXT1],
            )
        ),
    }
    kwargs = dict(command_name=COMMAND1, contexts=[CONTEXT1])
    command = Command(name=COMMAND1, args=[ARG1], help=COMMAND_HELP_STRING1)
    return configuration, kwargs, command


@case(tags=[SUCCESSFUL_TAG])
def case_read_successful_with_two_contexts(clear_configuration):
    Configuration.contexts_repository.add_contexts(
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
        Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2),
    )
    configuration = {
        COMMANDS: build_commands_builders_map(
            CommandBuilder(
                name=COMMAND1,
                help=COMMAND_HELP_STRING1,
                default_args=[ARG1],
                allowed_contexts=[CONTEXT1, CONTEXT2],
            )
        ),
    }
    kwargs = dict(command_name=COMMAND1, contexts=[CONTEXT1, CONTEXT2])
    command = Command(name=COMMAND1, args=[ARG1], help=COMMAND_HELP_STRING1)
    return configuration, kwargs, command


@case(tags=[SUCCESSFUL_TAG])
def case_with_context_specification(clear_configuration):
    Configuration.contexts_repository.add_contexts(
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
        Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2),
    )
    configuration = {
        COMMANDS: build_commands_builders_map(
            CommandBuilder(
                name=COMMAND1,
                help=COMMAND_HELP_STRING1,
                default_args=[ARG1, ARG2],
                contexts_specifications={
                    CONTEXT1: ContextSpecification(args=[ARG3, ARG4]),
                    CONTEXT2: ContextSpecification(args=[ARG5]),
                },
            )
        ),
    }
    kwargs = dict(command_name=COMMAND1, contexts=[CONTEXT1])
    command = Command(
        name=COMMAND1,
        args=[ARG3, ARG4],
        help=COMMAND_HELP_STRING1,
    )
    return configuration, kwargs, command


@case(tags=[SUCCESSFUL_TAG])
def case_with_clear_args_context(clear_configuration):
    Configuration.contexts_repository.add_contexts(
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
        Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2),
    )
    configuration = {
        COMMANDS: build_commands_builders_map(
            CommandBuilder(
                name=COMMAND1,
                help=COMMAND_HELP_STRING1,
                default_args=[ARG1, ARG2],
                contexts_specifications={
                    CONTEXT1: ContextSpecification(clear_args=True),
                    CONTEXT2: ContextSpecification(args=[ARG5]),
                },
            )
        ),
    }
    kwargs = dict(command_name=COMMAND1, contexts=[CONTEXT1])
    command = Command(name=COMMAND1, args=[], help=COMMAND_HELP_STRING1)
    return configuration, kwargs, command


@case(tags=[SUCCESSFUL_TAG])
def case_with_context_specification_add_args(clear_configuration):
    Configuration.contexts_repository.add_contexts(
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
        Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2),
    )
    configuration = {
        COMMANDS: build_commands_builders_map(
            CommandBuilder(
                name=COMMAND1,
                help=COMMAND_HELP_STRING1,
                default_args=[ARG1, ARG2],
                contexts_specifications={
                    CONTEXT1: ContextSpecification(add_args=[ARG3, ARG4]),
                    CONTEXT2: ContextSpecification(args=[ARG5]),
                },
            )
        ),
    }
    kwargs = dict(command_name=COMMAND1, contexts=[CONTEXT1])
    command = Command(
        name=COMMAND1,
        args=[ARG1, ARG2, ARG3, ARG4],
        help=COMMAND_HELP_STRING1,
    )
    return configuration, kwargs, command


@case(tags=[SUCCESSFUL_TAG])
def case_with_empty_allow_list(clear_configuration):
    configuration = {
        COMMANDS: build_commands_builders_map(
            CommandBuilder(
                name=COMMAND1, help=COMMAND_HELP_STRING1, default_args=[ARG1, ARG2]
            )
        ),
    }
    kwargs = dict(command_name=COMMAND1, allow_list=[])
    command = Command(name=COMMAND1, args=[ARG1, ARG2], help=COMMAND_HELP_STRING1)
    return configuration, kwargs, command


@case(tags=[SUCCESSFUL_TAG])
def case_in_allow_list(clear_configuration):
    configuration = {
        COMMANDS: build_commands_builders_map(
            CommandBuilder(
                name=COMMAND1, help=COMMAND_HELP_STRING1, default_args=[ARG1, ARG2]
            )
        ),
    }
    kwargs = dict(command_name=COMMAND1, allow_list=[COMMAND1])
    command = Command(name=COMMAND1, args=[ARG1, ARG2], help=COMMAND_HELP_STRING1)
    return configuration, kwargs, command


@case(tags=[SUCCESSFUL_TAG])
def case_not_in_deny_list(clear_configuration):
    configuration = {
        COMMANDS: build_commands_builders_map(
            CommandBuilder(
                name=COMMAND1, help=COMMAND_HELP_STRING1, default_args=[ARG1, ARG2]
            ),
            CommandBuilder(
                name=COMMAND2, help=COMMAND_HELP_STRING2, default_args=[ARG3]
            ),
        ),
    }
    kwargs = dict(command_name=COMMAND1, deny_list=[COMMAND2])
    command = Command(name=COMMAND1, args=[ARG1, ARG2], help=COMMAND_HELP_STRING1)
    return configuration, kwargs, command


@case(tags=[SUCCESSFUL_TAG])
def case_on_child_context_inheritance(clear_configuration):
    parent = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    context = Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2, parent=parent)
    Configuration.contexts_repository.add_contexts(parent, context)
    configuration = {
        COMMANDS: build_commands_builders_map(
            CommandBuilder(
                name=COMMAND1,
                help=COMMAND_HELP_STRING1,
                default_args=[ARG1, ARG2],
                contexts_specifications={CONTEXT1: ContextSpecification(args=[ARG3])},
            ),
        ),
    }
    kwargs = dict(command_name=COMMAND1, contexts=[CONTEXT2])
    command = Command(name=COMMAND1, args=[ARG3], help=COMMAND_HELP_STRING1)
    return configuration, kwargs, command


@case(tags=[SUCCESSFUL_TAG])
def case_context_alias(clear_configuration):
    Configuration.contexts_repository.add_contexts(
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING2, aliases=[CONTEXT2])
    )
    configuration = {
        COMMANDS: build_commands_builders_map(
            CommandBuilder(
                name=COMMAND1,
                help=COMMAND_HELP_STRING1,
                default_args=[ARG1, ARG2],
                contexts_specifications={CONTEXT2: ContextSpecification(args=[ARG3])},
            ),
        ),
    }
    kwargs = dict(command_name=COMMAND1, contexts=[CONTEXT2])
    command = Command(name=COMMAND1, args=[ARG3], help=COMMAND_HELP_STRING1)
    return configuration, kwargs, command


@case(tags=[SUCCESSFUL_TAG])
def case_with_one_required_context(clear_configuration):
    Configuration.contexts_repository.add_contexts(
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
        Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2),
    )
    configuration = {
        COMMANDS: build_commands_builders_map(
            CommandBuilder(
                name=COMMAND1,
                help=COMMAND_HELP_STRING1,
                default_args=[ARG1],
                required_contexts=[CONTEXT1],
            )
        ),
    }
    kwargs = dict(command_name=COMMAND1, contexts=[CONTEXT1])
    command = Command(name=COMMAND1, args=[ARG1], help=COMMAND_HELP_STRING1)
    return configuration, kwargs, command


@case(tags=[SUCCESSFUL_TAG])
def case_with_two_required_contexts(clear_configuration):
    Configuration.contexts_repository.add_contexts(
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
        Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2),
    )
    configuration = {
        COMMANDS: build_commands_builders_map(
            CommandBuilder(
                name=COMMAND1,
                help=COMMAND_HELP_STRING1,
                default_args=[ARG1],
                required_contexts=[CONTEXT1, CONTEXT2],
            )
        ),
    }
    kwargs = dict(command_name=COMMAND1, contexts=[CONTEXT1, CONTEXT2])
    command = Command(name=COMMAND1, args=[ARG1], help=COMMAND_HELP_STRING1)
    return configuration, kwargs, command


@parametrize_with_cases(
    argnames=["configuration", "kwargs", "command"],
    cases=THIS_MODULE,
    has_tag=SUCCESSFUL_TAG,
)
def test_read_command_success(configuration, kwargs, command, clear_configuration):
    Configuration.set_statue_configuration(configuration)
    actual_command = Configuration.read_command(**kwargs)
    assert actual_command == command, "Command is different than exp expected"


# Failure cases


@case(tags=[FAILED_TAG])
def case_with_non_existing_context(clear_configuration):
    configuration = {
        COMMANDS: build_commands_builders_map(
            CommandBuilder(
                name=COMMAND1,
                help=COMMAND_HELP_STRING1,
                default_args=[ARG1],
                contexts_specifications={
                    CONTEXT1: ContextSpecification(add_args=[ARG2, ARG3])
                },
            )
        ),
    }
    kwargs = dict(command_name=COMMAND1, contexts=[NOT_EXISTING_CONTEXT])
    return (
        configuration,
        kwargs,
        UnknownContext,
        f'^Could not find context named "{NOT_EXISTING_CONTEXT}"$',
    )


@case(tags=[FAILED_TAG])
def case_read_failed_with_two_contexts(clear_configuration):
    Configuration.contexts_repository.add_contexts(
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
        Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2),
    )
    configuration = {
        COMMANDS: build_commands_builders_map(
            CommandBuilder(
                name=COMMAND1,
                help=COMMAND_HELP_STRING1,
                default_args=[ARG1],
                allowed_contexts=[CONTEXT1],
            )
        ),
    }
    kwargs = dict(command_name=COMMAND1, contexts=[CONTEXT1, CONTEXT2])
    return (
        configuration,
        kwargs,
        InvalidCommand,
        f"^Command `{COMMAND1}`is not allowed "
        f"due to the following contexts: {CONTEXT2}",
    )


@case(tags=[FAILED_TAG])
def case_not_in_allow_list(clear_configuration):
    configuration = {
        COMMANDS: build_commands_builders_map(
            CommandBuilder(
                name=COMMAND1, help=COMMAND_HELP_STRING1, default_args=[ARG1, ARG2]
            ),
            CommandBuilder(
                name=COMMAND2, help=COMMAND_HELP_STRING2, default_args=[ARG3]
            ),
        ),
    }
    kwargs = dict(command_name=COMMAND1, allow_list=[COMMAND2])
    return (
        configuration,
        kwargs,
        InvalidCommand,
        f'Command "{COMMAND1}" was not specified in allowed list: {COMMAND2}',
    )


@case(tags=[FAILED_TAG])
def case_in_deny_list(clear_configuration):
    configuration = {
        COMMANDS: build_commands_builders_map(
            CommandBuilder(
                name=COMMAND1, help=COMMAND_HELP_STRING1, default_args=[ARG1, ARG2]
            ),
            CommandBuilder(
                name=COMMAND2, help=COMMAND_HELP_STRING2, default_args=[ARG3, ARG4]
            ),
        ),
    }
    kwargs = dict(command_name=COMMAND1, deny_list=[COMMAND1])
    return (
        configuration,
        kwargs,
        InvalidCommand,
        f'Command "{COMMAND1}" was explicitly denied in deny list: {COMMAND1}',
    )


@case(tags=[FAILED_TAG])
def case_non_existing_command(clear_configuration):
    configuration = {
        COMMANDS: build_commands_builders_map(
            CommandBuilder(
                name=COMMAND1, help=COMMAND_HELP_STRING1, default_args=[ARG1, ARG2]
            ),
            CommandBuilder(
                name=COMMAND2, help=COMMAND_HELP_STRING2, default_args=[ARG3, ARG5]
            ),
        ),
    }
    kwargs = dict(command_name=COMMAND3)
    return (
        configuration,
        kwargs,
        UnknownCommand,
        f'^Could not find command named "{COMMAND3}".$',
    )


@case(tags=[FAILED_TAG])
def case_with_no_commands_configuration(clear_configuration):
    configuration = {}
    kwargs = dict(command_name=COMMAND3)
    return (
        configuration,
        kwargs,
        MissingConfiguration,
        f'^"{COMMANDS}" is missing from Statue configuration.$',
    )


@case(tags=[FAILED_TAG])
def case_without_the_required_context(clear_configuration):
    configuration = {
        COMMANDS: build_commands_builders_map(
            CommandBuilder(
                name=COMMAND1,
                help=COMMAND_HELP_STRING1,
                default_args=[ARG1],
                required_contexts=[CONTEXT1],
            )
        ),
    }
    kwargs = dict(command_name=COMMAND1)
    return (
        configuration,
        kwargs,
        InvalidCommand,
        f"^Command `{COMMAND1}`requires the following contexts, "
        f"which are missing: {CONTEXT1}$",
    )


@case(tags=[FAILED_TAG])
def case_without_one_of_two_required_contexts(clear_configuration):
    Configuration.contexts_repository.add_contexts(
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
        Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2),
    )
    configuration = {
        COMMANDS: build_commands_builders_map(
            CommandBuilder(
                name=COMMAND1,
                help=COMMAND_HELP_STRING1,
                default_args=[ARG1],
                required_contexts=[CONTEXT1, CONTEXT2],
            )
        ),
    }
    kwargs = dict(command_name=COMMAND1, contexts=[CONTEXT1])
    return (
        configuration,
        kwargs,
        InvalidCommand,
        f"^Command `{COMMAND1}`requires the following contexts, "
        f"which are missing: {CONTEXT2}",
    )


@case(tags=[FAILED_TAG])
def case_without_two_required_contexts(clear_configuration):
    configuration = {
        COMMANDS: build_commands_builders_map(
            CommandBuilder(
                name=COMMAND1,
                help=COMMAND_HELP_STRING1,
                default_args=[ARG1],
                required_contexts=[CONTEXT1, CONTEXT2],
            )
        ),
    }
    kwargs = dict(command_name=COMMAND1)
    return (
        configuration,
        kwargs,
        InvalidCommand,
        f"^Command `{COMMAND1}`requires the following contexts, "
        f"which are missing: {CONTEXT1}, {CONTEXT2}",
    )


@parametrize_with_cases(
    argnames=["configuration", "kwargs", "exception_class", "exception_message"],
    cases=THIS_MODULE,
    has_tag=FAILED_TAG,
)
def test_read_command_failure(
    configuration, kwargs, exception_class, exception_message, clear_configuration
):
    Configuration.set_statue_configuration(configuration)
    with pytest.raises(expected_exception=exception_class, match=exception_message):
        Configuration.read_command(**kwargs)


# Additional tests


def test_read_command_multiple_times(clear_configuration):
    Configuration.contexts_repository.add_contexts(
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
        Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2),
        Context(name=CONTEXT3, help=CONTEXT_HELP_STRING3),
    )
    Configuration.set_statue_configuration(
        {
            COMMANDS: build_commands_builders_map(
                CommandBuilder(
                    name=COMMAND1,
                    help=COMMAND_HELP_STRING1,
                    default_args=[ARG1],
                    contexts_specifications={
                        CONTEXT1: ContextSpecification(add_args=[ARG2, ARG3]),
                        CONTEXT2: ContextSpecification(clear_args=True),
                        CONTEXT3: ContextSpecification(args=[ARG5]),
                    },
                )
            ),
        },
    )
    command1 = Configuration.read_command(command_name=COMMAND1, contexts=[CONTEXT1])
    assert command1 == Command(
        name=COMMAND1, help=COMMAND_HELP_STRING1, args=[ARG1, ARG2, ARG3]
    ), "Command is different than expected in first read."

    command2 = Configuration.read_command(command_name=COMMAND1)
    assert command2 == Command(
        name=COMMAND1, help=COMMAND_HELP_STRING1, args=[ARG1]
    ), "Command is different than expected in second read."

    command3 = Configuration.read_command(command_name=COMMAND1, contexts=[CONTEXT2])
    assert command3 == Command(
        name=COMMAND1, help=COMMAND_HELP_STRING1, args=[]
    ), "Command is different than expected in forth read."

    command4 = Configuration.read_command(command_name=COMMAND1, contexts=[CONTEXT3])
    assert command4 == Command(
        name=COMMAND1, help=COMMAND_HELP_STRING1, args=[ARG5]
    ), "Command is different than expected in third read."
