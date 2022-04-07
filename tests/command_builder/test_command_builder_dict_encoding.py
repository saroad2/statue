from collections import OrderedDict

import pytest
from pytest_cases import THIS_MODULE, case, parametrize_with_cases

from statue.command_builder import CommandBuilder, ContextSpecification
from statue.config.contexts_repository import ContextsRepository
from statue.constants import (
    ADD_ARGS,
    ALLOWED_CONTEXTS,
    ARGS,
    CLEAR_ARGS,
    HELP,
    REQUIRED_CONTEXTS,
    VERSION,
)
from statue.context import Context
from statue.exceptions import InconsistentConfiguration
from tests.constants import (
    ARG1,
    ARG2,
    ARG3,
    ARG4,
    COMMAND1,
    COMMAND_HELP_STRING1,
    COMMAND_HELP_STRING2,
    CONTEXT1,
    CONTEXT2,
    CONTEXT3,
    CONTEXT4,
    CONTEXT5,
    CONTEXT6,
    CONTEXT_HELP_STRING1,
    CONTEXT_HELP_STRING2,
    CONTEXT_HELP_STRING3,
    CONTEXT_HELP_STRING4,
    CONTEXT_HELP_STRING5,
    CONTEXT_HELP_STRING6,
    FAILED_TAG,
    SUCCESSFUL_TAG,
)

# Successful tests
from tests.util import dummy_version


@case(tags=[SUCCESSFUL_TAG])
def case_simple_command_builder_from_dict():
    command_builder_dict = OrderedDict([(HELP, COMMAND_HELP_STRING1)])
    command_builder = CommandBuilder(name=COMMAND1, help=COMMAND_HELP_STRING1)
    contexts_repository = ContextsRepository()

    return command_builder_dict, command_builder, contexts_repository


@case(tags=[SUCCESSFUL_TAG])
def case_command_builder_from_dict_with_version():
    version = dummy_version()
    command_builder_dict = OrderedDict(
        [(HELP, COMMAND_HELP_STRING1), (VERSION, version)]
    )
    command_builder = CommandBuilder(
        name=COMMAND1, help=COMMAND_HELP_STRING1, version=version
    )
    contexts_repository = ContextsRepository()

    return command_builder_dict, command_builder, contexts_repository


@case(tags=[SUCCESSFUL_TAG])
def case_command_builder_from_dict_with_default_args():
    command_builder_dict = OrderedDict(
        [(HELP, COMMAND_HELP_STRING1), (ARGS, [ARG1, ARG2])]
    )
    command_builder = CommandBuilder(
        name=COMMAND1, help=COMMAND_HELP_STRING1, default_args=[ARG1, ARG2]
    )
    contexts_repository = ContextsRepository()

    return command_builder_dict, command_builder, contexts_repository


@case(tags=[SUCCESSFUL_TAG])
def case_command_builder_from_dict_with_required_contexts():
    context1, context2 = (
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
        Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2),
    )
    command_builder_dict = OrderedDict(
        [(HELP, COMMAND_HELP_STRING1), (REQUIRED_CONTEXTS, [CONTEXT1, CONTEXT2])]
    )
    command_builder = CommandBuilder(
        name=COMMAND1, help=COMMAND_HELP_STRING1, required_contexts=[context1, context2]
    )
    contexts_repository = ContextsRepository(context1, context2)

    return command_builder_dict, command_builder, contexts_repository


@case(tags=[SUCCESSFUL_TAG])
def case_command_builder_from_dict_with_allowed_contexts():
    context1, context2 = (
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
        Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2),
    )
    command_builder_dict = OrderedDict(
        [(HELP, COMMAND_HELP_STRING1), (ALLOWED_CONTEXTS, [CONTEXT1, CONTEXT2])]
    )
    command_builder = CommandBuilder(
        name=COMMAND1, help=COMMAND_HELP_STRING1, allowed_contexts=[context1, context2]
    )
    contexts_repository = ContextsRepository(context1, context2)

    return command_builder_dict, command_builder, contexts_repository


@case(tags=[SUCCESSFUL_TAG])
def case_command_builder_from_dict_with_args_override():
    context = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    command_builder_dict = OrderedDict(
        [
            (HELP, COMMAND_HELP_STRING1),
            (ARGS, [ARG1, ARG2]),
            (CONTEXT1, {ARGS: [ARG3, ARG4]}),
        ]
    )
    command_builder = CommandBuilder(
        name=COMMAND1,
        help=COMMAND_HELP_STRING1,
        default_args=[ARG1, ARG2],
        contexts_specifications={context: ContextSpecification(args=[ARG3, ARG4])},
    )
    contexts_repository = ContextsRepository(context)

    return command_builder_dict, command_builder, contexts_repository


@case(tags=[SUCCESSFUL_TAG])
def case_command_builder_from_dict_with_added_args():
    context = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    command_builder_dict = OrderedDict(
        [
            (HELP, COMMAND_HELP_STRING1),
            (ARGS, [ARG1, ARG2]),
            (CONTEXT1, {ADD_ARGS: [ARG3, ARG4]}),
        ]
    )
    command_builder = CommandBuilder(
        name=COMMAND1,
        help=COMMAND_HELP_STRING1,
        default_args=[ARG1, ARG2],
        contexts_specifications={context: ContextSpecification(add_args=[ARG3, ARG4])},
    )
    contexts_repository = ContextsRepository(context)

    return command_builder_dict, command_builder, contexts_repository


@case(tags=[SUCCESSFUL_TAG])
def case_command_builder_from_dict_with_clear_args():
    context = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    command_builder_dict = OrderedDict(
        [
            (HELP, COMMAND_HELP_STRING1),
            (ARGS, [ARG1, ARG2]),
            (CONTEXT1, {CLEAR_ARGS: True}),
        ]
    )
    command_builder = CommandBuilder(
        name=COMMAND1,
        help=COMMAND_HELP_STRING1,
        default_args=[ARG1, ARG2],
        contexts_specifications={context: ContextSpecification(clear_args=True)},
    )
    contexts_repository = ContextsRepository(context)

    return command_builder_dict, command_builder, contexts_repository


@case(tags=[SUCCESSFUL_TAG])
def case_command_builder_from_dict_with_two_contexts_specifications():
    context1, context2 = (
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
        Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2),
    )
    command_builder_dict = OrderedDict(
        [
            (HELP, COMMAND_HELP_STRING1),
            (ARGS, [ARG1, ARG2]),
            (CONTEXT1, {CLEAR_ARGS: True}),
            (CONTEXT2, {ADD_ARGS: [ARG3, ARG4]}),
        ]
    )
    command_builder = CommandBuilder(
        name=COMMAND1,
        help=COMMAND_HELP_STRING1,
        default_args=[ARG1, ARG2],
        contexts_specifications={
            context1: ContextSpecification(clear_args=True),
            context2: ContextSpecification(add_args=[ARG3, ARG4]),
        },
    )
    contexts_repository = ContextsRepository(context1, context2)

    return command_builder_dict, command_builder, contexts_repository


@case(tags=[SUCCESSFUL_TAG])
def case_command_builder_from_dict_with_everything():
    context1, context2, context3, context4, context5, context6 = (
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
        Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2),
        Context(name=CONTEXT3, help=CONTEXT_HELP_STRING3),
        Context(name=CONTEXT4, help=CONTEXT_HELP_STRING4),
        Context(name=CONTEXT5, help=CONTEXT_HELP_STRING5),
        Context(name=CONTEXT6, help=CONTEXT_HELP_STRING6),
    )
    version = dummy_version()
    command_builder_dict = OrderedDict(
        [
            (HELP, COMMAND_HELP_STRING1),
            (ARGS, [ARG1, ARG2]),
            (REQUIRED_CONTEXTS, [CONTEXT3, CONTEXT4]),
            (ALLOWED_CONTEXTS, [CONTEXT1, CONTEXT2]),
            (VERSION, version),
            (CONTEXT5, {CLEAR_ARGS: True}),
            (CONTEXT6, {ADD_ARGS: [ARG3, ARG4]}),
        ]
    )
    command_builder = CommandBuilder(
        name=COMMAND1,
        help=COMMAND_HELP_STRING1,
        version=version,
        default_args=[ARG1, ARG2],
        allowed_contexts=[context1, context2],
        required_contexts=[context3, context4],
        contexts_specifications={
            context5: ContextSpecification(clear_args=True),
            context6: ContextSpecification(add_args=[ARG3, ARG4]),
        },
    )
    contexts_repository = ContextsRepository(
        context1, context2, context3, context4, context5, context6
    )

    return command_builder_dict, command_builder, contexts_repository


@parametrize_with_cases(
    argnames=["command_builder_dict", "command_builder", "contexts_repository"],
    cases=THIS_MODULE,
    has_tag=SUCCESSFUL_TAG,
)
def test_command_builder_from_dict_successful(
    command_builder_dict, command_builder, contexts_repository
):
    actual_builder = CommandBuilder.from_dict(
        command_name=COMMAND1,
        builder_setups=command_builder_dict,
        contexts_repository=contexts_repository,
    )
    assert actual_builder == command_builder


@parametrize_with_cases(
    argnames=["command_builder_dict", "command_builder"],
    cases=THIS_MODULE,
    has_tag=SUCCESSFUL_TAG,
)
def test_command_builder_as_dict_successful(command_builder_dict, command_builder):
    actual_command_builder_dict = command_builder.as_dict()
    assert isinstance(actual_command_builder_dict, OrderedDict)
    assert list(actual_command_builder_dict.keys()) == list(command_builder_dict.keys())
    assert actual_command_builder_dict == command_builder_dict


# Failed tests


@case(tags=[FAILED_TAG])
def case_command_builder_from_dict_fail_on_both_clear_args_and_args():
    command_builder_dict = {
        HELP: COMMAND_HELP_STRING1,
        CONTEXT1: {ARGS: [ARG1, ARG2], CLEAR_ARGS: True},
    }
    contexts_repository = ContextsRepository(
        Context(name=CONTEXT1, help=COMMAND_HELP_STRING1)
    )
    error_message = (
        f"Inconsistency in {COMMAND1} context specification for {CONTEXT1}: "
        f"clear_args and args cannot be both set at the same time"
    )

    return command_builder_dict, contexts_repository, error_message


@case(tags=[FAILED_TAG])
def case_command_builder_from_dict_fail_on_both_clear_args_and_add_args():
    command_builder_dict = {
        HELP: COMMAND_HELP_STRING1,
        CONTEXT1: {ADD_ARGS: [ARG1, ARG2], CLEAR_ARGS: True},
    }
    contexts_repository = ContextsRepository(
        Context(name=CONTEXT1, help=COMMAND_HELP_STRING1)
    )
    error_message = (
        f"Inconsistency in {COMMAND1} context specification for {CONTEXT1}: "
        f"clear_args and add_args cannot be both set at the same time"
    )

    return command_builder_dict, contexts_repository, error_message


@case(tags=[FAILED_TAG])
def case_command_builder_from_dict_fail_on_both_args_and_add_args():
    command_builder_dict = {
        HELP: COMMAND_HELP_STRING1,
        CONTEXT1: {ARGS: [ARG1, ARG2], ADD_ARGS: [ARG3, ARG4]},
    }
    contexts_repository = ContextsRepository(
        Context(name=CONTEXT1, help=COMMAND_HELP_STRING1)
    )
    error_message = (
        f"Inconsistency in {COMMAND1} context specification for {CONTEXT1}: "
        f"args and add_args cannot be both set at the same time"
    )

    return command_builder_dict, contexts_repository, error_message


@case(tags=[FAILED_TAG])
def case_command_builder_from_dict_fail_unknown_required_context():
    command_builder_dict = {
        HELP: COMMAND_HELP_STRING1,
        REQUIRED_CONTEXTS: [CONTEXT1],
    }
    contexts_repository = ContextsRepository(
        Context(name=CONTEXT2, help=COMMAND_HELP_STRING2)
    )
    error_message = (
        f"The following contexts defined in {REQUIRED_CONTEXTS} "
        f"for {COMMAND1} command are not defined in configuration: {CONTEXT1}"
    )

    return command_builder_dict, contexts_repository, error_message


@case(tags=[FAILED_TAG])
def case_command_builder_from_dict_fail_unknown_allowed_context():
    command_builder_dict = {
        HELP: COMMAND_HELP_STRING1,
        ALLOWED_CONTEXTS: [CONTEXT1],
    }
    contexts_repository = ContextsRepository(
        Context(name=CONTEXT2, help=COMMAND_HELP_STRING2)
    )
    error_message = (
        f"The following contexts defined in {ALLOWED_CONTEXTS} "
        f"for {COMMAND1} command are not defined in configuration: {CONTEXT1}"
    )

    return command_builder_dict, contexts_repository, error_message


@case(tags=[FAILED_TAG])
def case_command_builder_from_dict_fail_unknown_specified_context():
    command_builder_dict = {
        HELP: COMMAND_HELP_STRING1,
        CONTEXT1: {ARGS: [ARG1, ARG2]},
    }
    contexts_repository = ContextsRepository(
        Context(name=CONTEXT2, help=COMMAND_HELP_STRING2)
    )
    error_message = (
        f"The following specified contexts defined in {COMMAND1} "
        f"are not defined in configuration: {CONTEXT1}"
    )

    return command_builder_dict, contexts_repository, error_message


@parametrize_with_cases(
    argnames=["command_builder_dict", "contexts_repository", "error_message"],
    cases=THIS_MODULE,
    has_tag=FAILED_TAG,
)
def test_command_builder_from_dict_failed(
    command_builder_dict, contexts_repository, error_message
):
    with pytest.raises(InconsistentConfiguration, match=f"^{error_message}$"):
        CommandBuilder.from_dict(
            command_name=COMMAND1,
            builder_setups=command_builder_dict,
            contexts_repository=contexts_repository,
        )
