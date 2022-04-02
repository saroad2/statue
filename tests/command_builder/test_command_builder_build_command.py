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
    CONTEXT_HELP_STRING3,
    CONTEXT_HELP_STRING4,
    FAILED_TAG,
    SUCCESSFUL_TAG,
)

# Successful tests
from tests.util import dummy_version


@case(tags=SUCCESSFUL_TAG)
def case_simple_command_builder():
    command_builder = CommandBuilder(name=COMMAND1, help=COMMAND_HELP_STRING1)
    contexts = []
    command = Command(name=COMMAND1)

    return command_builder, contexts, command


@case(tags=SUCCESSFUL_TAG)
def case_command_builder_with_default_args():
    command_builder = CommandBuilder(
        name=COMMAND1, help=COMMAND_HELP_STRING1, default_args=[ARG1, ARG2]
    )
    contexts = []
    command = Command(name=COMMAND1, args=[ARG1, ARG2])

    return command_builder, contexts, command


@case(tags=SUCCESSFUL_TAG)
def case_command_builder_with_version():
    version = dummy_version()
    command_builder = CommandBuilder(
        name=COMMAND1, help=COMMAND_HELP_STRING1, version=version
    )
    contexts = []
    command = Command(name=COMMAND1)

    return command_builder, contexts, command


@case(tags=SUCCESSFUL_TAG)
def case_command_builder_with_allowed_context():
    context = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    command_builder = CommandBuilder(
        name=COMMAND1, help=COMMAND_HELP_STRING1, allowed_contexts=[context]
    )
    command = Command(name=COMMAND1)

    return command_builder, [context], command


@case(tags=SUCCESSFUL_TAG)
def case_command_builder_with_allowed_context_by_default():
    command_builder = CommandBuilder(name=COMMAND1, help=COMMAND_HELP_STRING1)
    contexts = [
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1, allowed_by_default=True)
    ]
    command = Command(name=COMMAND1)

    return command_builder, contexts, command


@case(tags=SUCCESSFUL_TAG)
def case_command_builder_with_required_context():
    context = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    command_builder = CommandBuilder(
        name=COMMAND1, help=COMMAND_HELP_STRING1, required_contexts=[context]
    )
    command = Command(name=COMMAND1)

    return command_builder, [context], command


@case(tags=SUCCESSFUL_TAG)
def case_command_builder_with_overriding_args():
    context = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    command_builder = CommandBuilder(
        name=COMMAND1,
        help=COMMAND_HELP_STRING1,
        default_args=[ARG1, ARG2],
        contexts_specifications={
            context: ContextSpecification(args=[ARG3, ARG4, ARG5])
        },
    )
    command = Command(name=COMMAND1, args=[ARG3, ARG4, ARG5])

    return command_builder, [context], command


@case(tags=SUCCESSFUL_TAG)
def case_command_builder_with_added_args():
    context = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    command_builder = CommandBuilder(
        name=COMMAND1,
        help=COMMAND_HELP_STRING1,
        default_args=[ARG1, ARG2],
        contexts_specifications={context: ContextSpecification(add_args=[ARG3, ARG4])},
    )
    command = Command(name=COMMAND1, args=[ARG1, ARG2, ARG3, ARG4])

    return command_builder, [context], command


@case(tags=SUCCESSFUL_TAG)
def case_command_builder_with_clear_args():
    context = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    command_builder = CommandBuilder(
        name=COMMAND1,
        help=COMMAND_HELP_STRING1,
        default_args=[ARG1, ARG2],
        contexts_specifications={context: ContextSpecification(clear_args=True)},
    )
    command = Command(name=COMMAND1)

    return command_builder, [context], command


@case(tags=SUCCESSFUL_TAG)
def case_command_builder_with_two_added_args_contexts():
    context1 = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    context2 = Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2)
    command_builder = CommandBuilder(
        name=COMMAND1,
        help=COMMAND_HELP_STRING1,
        default_args=[ARG1, ARG2],
        contexts_specifications={
            context1: ContextSpecification(add_args=[ARG3, ARG4]),
            context2: ContextSpecification(add_args=[ARG5, ARG6]),
        },
    )
    command = Command(
        name=COMMAND1,
        args=[ARG1, ARG2, ARG3, ARG4, ARG5, ARG6],
    )

    return command_builder, [context1, context2], command


@case(tags=SUCCESSFUL_TAG)
def case_command_builder_with_add_and_clear_contexts():
    context1 = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    context2 = Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2)
    command_builder = CommandBuilder(
        name=COMMAND1,
        help=COMMAND_HELP_STRING1,
        default_args=[ARG1, ARG2],
        contexts_specifications={
            context1: ContextSpecification(add_args=[ARG3, ARG4]),
            context2: ContextSpecification(clear_args=True),
        },
    )
    command = Command(name=COMMAND1)

    return command_builder, [context1, context2], command


@parametrize_with_cases(
    argnames=["command_builder", "contexts", "command"],
    cases=THIS_MODULE,
    has_tag=SUCCESSFUL_TAG,
)
def test_command_builder_build_command_successfully(command_builder, contexts, command):
    assert command_builder.build_command(*contexts) == command


@parametrize_with_cases(
    argnames=["command_builder", "contexts", "command"],
    cases=THIS_MODULE,
    has_tag=SUCCESSFUL_TAG,
)
def test_command_builder_match_contexts(command_builder, contexts, command):
    assert command_builder.match_contexts(*contexts)


# Failure tests


@case(tags=FAILED_TAG)
def case_command_builder_missing_required_context():
    context1 = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    context2 = Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2)
    command_builder = CommandBuilder(
        name=COMMAND1, help=COMMAND_HELP_STRING1, required_contexts=[context1]
    )
    error_message = (
        f"Command `{COMMAND1}`requires the following contexts, "
        f"which are missing: {CONTEXT1}"
    )

    return command_builder, [context2], error_message


@case(tags=FAILED_TAG)
def case_command_builder_with_not_allowed_context():
    context1 = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    context2 = Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2)
    context3 = Context(name=CONTEXT3, help=CONTEXT_HELP_STRING3)
    context4 = Context(name=CONTEXT4, help=CONTEXT_HELP_STRING4)
    command_builder = CommandBuilder(
        name=COMMAND1,
        help=COMMAND_HELP_STRING1,
        required_contexts=[context2],
        allowed_contexts=[context3],
        contexts_specifications={context4: ContextSpecification(args=[ARG1, ARG2])},
    )
    error_message = (
        f"Command `{COMMAND1}`is not allowed due to the following contexts: {CONTEXT1}"
    )

    return command_builder, [context1, context2], error_message


@parametrize_with_cases(
    argnames=["command_builder", "contexts", "error_message"],
    cases=THIS_MODULE,
    has_tag=FAILED_TAG,
)
def test_command_builder_build_command_failed(command_builder, contexts, error_message):
    with pytest.raises(InvalidCommand, match=f"^{error_message}$"):
        command_builder.build_command(*contexts)


@parametrize_with_cases(
    argnames=["command_builder", "contexts", "error_message"],
    cases=THIS_MODULE,
    has_tag=FAILED_TAG,
)
def test_command_builder_does_not_match_contexts(
    command_builder, contexts, error_message
):
    assert not command_builder.match_contexts(*contexts)
