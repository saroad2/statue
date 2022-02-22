import pytest
from pytest_cases import THIS_MODULE, case, parametrize_with_cases

from statue.command import Command
from statue.command_builder import CommandBuilder, ContextSpecification
from statue.context import Context
from statue.exceptions import InvalidCommand
from tests.constants import (
    ARG1,
    ARG2,
    ARG3,
    ARG4,
    ARG5,
    ARG6,
    COMMAND1,
    COMMAND_HELP_STRING1,
    CONTEXT1,
    CONTEXT2,
    CONTEXT3,
    CONTEXT4,
    CONTEXT_HELP_STRING1,
    CONTEXT_HELP_STRING2,
    FAILED_TAG,
    SUCCESSFUL_TAG,
)

# Successful tests


@case(tags=SUCCESSFUL_TAG)
def case_simple_command_builder():
    command_builder = CommandBuilder(name=COMMAND1, help=COMMAND_HELP_STRING1)
    contexts = []
    command = Command(name=COMMAND1, help=COMMAND_HELP_STRING1)

    return command_builder, contexts, command


@case(tags=SUCCESSFUL_TAG)
def case_command_builder_with_default_args():
    command_builder = CommandBuilder(
        name=COMMAND1, help=COMMAND_HELP_STRING1, default_args=[ARG1, ARG2]
    )
    contexts = []
    command = Command(name=COMMAND1, help=COMMAND_HELP_STRING1, args=[ARG1, ARG2])

    return command_builder, contexts, command


@case(tags=SUCCESSFUL_TAG)
def case_command_builder_with_version():
    version = "1.2.3"
    command_builder = CommandBuilder(
        name=COMMAND1, help=COMMAND_HELP_STRING1, version=version
    )
    contexts = []
    command = Command(name=COMMAND1, help=COMMAND_HELP_STRING1, version=version)

    return command_builder, contexts, command


@case(tags=SUCCESSFUL_TAG)
def case_command_builder_with_allowed_context():
    command_builder = CommandBuilder(
        name=COMMAND1, help=COMMAND_HELP_STRING1, allowed_contexts=[CONTEXT1]
    )
    contexts = [Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)]
    command = Command(name=COMMAND1, help=COMMAND_HELP_STRING1)

    return command_builder, contexts, command


@case(tags=SUCCESSFUL_TAG)
def case_command_builder_with_required_context():
    command_builder = CommandBuilder(
        name=COMMAND1, help=COMMAND_HELP_STRING1, required_contexts=[CONTEXT1]
    )
    contexts = [Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)]
    command = Command(name=COMMAND1, help=COMMAND_HELP_STRING1)

    return command_builder, contexts, command


@case(tags=SUCCESSFUL_TAG)
def case_command_builder_with_overriding_args():
    command_builder = CommandBuilder(
        name=COMMAND1,
        help=COMMAND_HELP_STRING1,
        default_args=[ARG1, ARG2],
        contexts_specifications={
            CONTEXT1: ContextSpecification(args=[ARG3, ARG4, ARG5])
        },
    )
    contexts = [Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)]
    command = Command(name=COMMAND1, help=COMMAND_HELP_STRING1, args=[ARG3, ARG4, ARG5])

    return command_builder, contexts, command


@case(tags=SUCCESSFUL_TAG)
def case_command_builder_with_added_args():
    command_builder = CommandBuilder(
        name=COMMAND1,
        help=COMMAND_HELP_STRING1,
        default_args=[ARG1, ARG2],
        contexts_specifications={CONTEXT1: ContextSpecification(add_args=[ARG3, ARG4])},
    )
    contexts = [Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)]
    command = Command(
        name=COMMAND1, help=COMMAND_HELP_STRING1, args=[ARG1, ARG2, ARG3, ARG4]
    )

    return command_builder, contexts, command


@case(tags=SUCCESSFUL_TAG)
def case_command_builder_with_clear_args():
    command_builder = CommandBuilder(
        name=COMMAND1,
        help=COMMAND_HELP_STRING1,
        default_args=[ARG1, ARG2],
        contexts_specifications={CONTEXT1: ContextSpecification(clear_args=True)},
    )
    contexts = [Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)]
    command = Command(name=COMMAND1, help=COMMAND_HELP_STRING1)

    return command_builder, contexts, command


@case(tags=SUCCESSFUL_TAG)
def case_command_builder_with_two_added_args_contexts():
    command_builder = CommandBuilder(
        name=COMMAND1,
        help=COMMAND_HELP_STRING1,
        default_args=[ARG1, ARG2],
        contexts_specifications={
            CONTEXT1: ContextSpecification(add_args=[ARG3, ARG4]),
            CONTEXT2: ContextSpecification(add_args=[ARG5, ARG6]),
        },
    )
    contexts = [
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
        Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2),
    ]
    command = Command(
        name=COMMAND1,
        help=COMMAND_HELP_STRING1,
        args=[ARG1, ARG2, ARG3, ARG4, ARG5, ARG6],
    )

    return command_builder, contexts, command


@case(tags=SUCCESSFUL_TAG)
def case_command_builder_with_add_and_clear_contexts():
    command_builder = CommandBuilder(
        name=COMMAND1,
        help=COMMAND_HELP_STRING1,
        default_args=[ARG1, ARG2],
        contexts_specifications={
            CONTEXT1: ContextSpecification(add_args=[ARG3, ARG4]),
            CONTEXT2: ContextSpecification(clear_args=True),
        },
    )
    contexts = [
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
        Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2),
    ]
    command = Command(name=COMMAND1, help=COMMAND_HELP_STRING1)

    return command_builder, contexts, command


@parametrize_with_cases(
    argnames=["command_builder", "contexts", "command"],
    cases=THIS_MODULE,
    has_tag=SUCCESSFUL_TAG,
)
def test_command_builder_build_command_successfully(command_builder, contexts, command):
    assert command_builder.build_command(*contexts) == command


# Successful tests


@case(tags=FAILED_TAG)
def case_command_builder_missing_required_context():
    command_builder = CommandBuilder(
        name=COMMAND1, help=COMMAND_HELP_STRING1, required_contexts=[CONTEXT1]
    )
    contexts = [Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2)]
    error_message = (
        f"Command `{COMMAND1}`requires the following contexts, "
        f"which are missing: {CONTEXT1}"
    )

    return command_builder, contexts, error_message


@case(tags=FAILED_TAG)
def case_command_builder_with_not_allowed_context():
    command_builder = CommandBuilder(
        name=COMMAND1,
        help=COMMAND_HELP_STRING1,
        required_contexts=[CONTEXT2],
        allowed_contexts=[CONTEXT3],
        contexts_specifications={CONTEXT4: ContextSpecification(args=[ARG1, ARG2])},
    )
    contexts = [
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
        Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2),
    ]
    error_message = (
        f"Command `{COMMAND1}`is not allowed due to the following contexts: {CONTEXT1}"
    )

    return command_builder, contexts, error_message


@parametrize_with_cases(
    argnames=["command_builder", "contexts", "error_message"],
    cases=THIS_MODULE,
    has_tag=FAILED_TAG,
)
def test_command_builder_build_command_failed(command_builder, contexts, error_message):
    with pytest.raises(InvalidCommand, match=f"^{error_message}$"):
        command_builder.build_command(*contexts)
