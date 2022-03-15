import pytest
from pytest_cases import THIS_MODULE, case, parametrize_with_cases

from statue.command_builder import CommandBuilder, ContextSpecification
from statue.constants import (
    ADD_ARGS,
    ALLOWED_CONTEXTS,
    ARGS,
    CLEAR_ARGS,
    HELP,
    REQUIRED_CONTEXTS,
    VERSION,
)
from statue.exceptions import InconsistentConfiguration
from tests.constants import (
    ARG1,
    ARG2,
    ARG3,
    ARG4,
    COMMAND1,
    COMMAND_HELP_STRING1,
    CONTEXT1,
    CONTEXT2,
    CONTEXT3,
    CONTEXT4,
    CONTEXT5,
    CONTEXT6,
    FAILED_TAG,
    SUCCESSFUL_TAG,
)

# Successful tests


@case(tags=[SUCCESSFUL_TAG])
def case_simple_command_builder_from_dict():
    command_builder_dict = {HELP: COMMAND_HELP_STRING1}
    command_builder = CommandBuilder(name=COMMAND1, help=COMMAND_HELP_STRING1)

    return command_builder_dict, command_builder


@case(tags=[SUCCESSFUL_TAG])
def case_command_builder_from_dict_with_version():
    version = "7.1.4"
    command_builder_dict = {HELP: COMMAND_HELP_STRING1, VERSION: version}
    command_builder = CommandBuilder(
        name=COMMAND1, help=COMMAND_HELP_STRING1, version=version
    )

    return command_builder_dict, command_builder


@case(tags=[SUCCESSFUL_TAG])
def case_command_builder_from_dict_with_default_args():
    command_builder_dict = {HELP: COMMAND_HELP_STRING1, ARGS: [ARG1, ARG2]}
    command_builder = CommandBuilder(
        name=COMMAND1, help=COMMAND_HELP_STRING1, default_args=[ARG1, ARG2]
    )

    return command_builder_dict, command_builder


@case(tags=[SUCCESSFUL_TAG])
def case_command_builder_from_dict_with_required_contexts():
    command_builder_dict = {
        HELP: COMMAND_HELP_STRING1,
        REQUIRED_CONTEXTS: [CONTEXT1, CONTEXT2],
    }
    command_builder = CommandBuilder(
        name=COMMAND1, help=COMMAND_HELP_STRING1, required_contexts=[CONTEXT1, CONTEXT2]
    )

    return command_builder_dict, command_builder


@case(tags=[SUCCESSFUL_TAG])
def case_command_builder_from_dict_with_allowed_contexts():
    command_builder_dict = {
        HELP: COMMAND_HELP_STRING1,
        ALLOWED_CONTEXTS: [CONTEXT1, CONTEXT2],
    }
    command_builder = CommandBuilder(
        name=COMMAND1, help=COMMAND_HELP_STRING1, allowed_contexts=[CONTEXT1, CONTEXT2]
    )

    return command_builder_dict, command_builder


@case(tags=[SUCCESSFUL_TAG])
def case_command_builder_from_dict_with_args_override():
    command_builder_dict = {
        HELP: COMMAND_HELP_STRING1,
        ARGS: [ARG1, ARG2],
        CONTEXT1: {ARGS: [ARG3, ARG4]},
    }
    command_builder = CommandBuilder(
        name=COMMAND1,
        help=COMMAND_HELP_STRING1,
        default_args=[ARG1, ARG2],
        contexts_specifications={CONTEXT1: ContextSpecification(args=[ARG3, ARG4])},
    )

    return command_builder_dict, command_builder


@case(tags=[SUCCESSFUL_TAG])
def case_command_builder_from_dict_with_added_args():
    command_builder_dict = {
        HELP: COMMAND_HELP_STRING1,
        ARGS: [ARG1, ARG2],
        CONTEXT1: {ADD_ARGS: [ARG3, ARG4]},
    }
    command_builder = CommandBuilder(
        name=COMMAND1,
        help=COMMAND_HELP_STRING1,
        default_args=[ARG1, ARG2],
        contexts_specifications={CONTEXT1: ContextSpecification(add_args=[ARG3, ARG4])},
    )

    return command_builder_dict, command_builder


@case(tags=[SUCCESSFUL_TAG])
def case_command_builder_from_dict_with_clear_args():
    command_builder_dict = {
        HELP: COMMAND_HELP_STRING1,
        ARGS: [ARG1, ARG2],
        CONTEXT1: {CLEAR_ARGS: True},
    }
    command_builder = CommandBuilder(
        name=COMMAND1,
        help=COMMAND_HELP_STRING1,
        default_args=[ARG1, ARG2],
        contexts_specifications={CONTEXT1: ContextSpecification(clear_args=True)},
    )

    return command_builder_dict, command_builder


@case(tags=[SUCCESSFUL_TAG])
def case_command_builder_from_dict_with_two_contexts_specifications():
    command_builder_dict = {
        HELP: COMMAND_HELP_STRING1,
        ARGS: [ARG1, ARG2],
        CONTEXT1: {CLEAR_ARGS: True},
        CONTEXT2: {ADD_ARGS: [ARG3, ARG4]},
    }
    command_builder = CommandBuilder(
        name=COMMAND1,
        help=COMMAND_HELP_STRING1,
        default_args=[ARG1, ARG2],
        contexts_specifications={
            CONTEXT1: ContextSpecification(clear_args=True),
            CONTEXT2: ContextSpecification(add_args=[ARG3, ARG4]),
        },
    )

    return command_builder_dict, command_builder


@case(tags=[SUCCESSFUL_TAG])
def case_command_builder_from_dict_with_verything():
    version = "5.2.6"
    command_builder_dict = {
        HELP: COMMAND_HELP_STRING1,
        ARGS: [ARG1, ARG2],
        VERSION: version,
        ALLOWED_CONTEXTS: [CONTEXT1, CONTEXT2],
        REQUIRED_CONTEXTS: [CONTEXT3, CONTEXT4],
        CONTEXT5: {CLEAR_ARGS: True},
        CONTEXT6: {ADD_ARGS: [ARG3, ARG4]},
    }
    command_builder = CommandBuilder(
        name=COMMAND1,
        help=COMMAND_HELP_STRING1,
        version=version,
        default_args=[ARG1, ARG2],
        allowed_contexts=[CONTEXT1, CONTEXT2],
        required_contexts=[CONTEXT3, CONTEXT4],
        contexts_specifications={
            CONTEXT5: ContextSpecification(clear_args=True),
            CONTEXT6: ContextSpecification(add_args=[ARG3, ARG4]),
        },
    )

    return command_builder_dict, command_builder


@parametrize_with_cases(
    argnames=["command_builder_dict", "command_builder"],
    cases=THIS_MODULE,
    has_tag=SUCCESSFUL_TAG,
)
def test_command_builder_from_dict_successful(command_builder_dict, command_builder):
    actual_builder = CommandBuilder.from_dict(
        command_name=COMMAND1, builder_setups=command_builder_dict
    )
    assert actual_builder == command_builder


# Failed tests


@case(tags=[FAILED_TAG])
def case_command_builder_from_dict_fail_on_both_clear_args_and_args():
    command_builder_dict = {
        HELP: COMMAND_HELP_STRING1,
        CONTEXT1: {ARGS: [ARG1, ARG2], CLEAR_ARGS: True},
    }
    error_message = (
        f"Inconsistency in {COMMAND1} context specification for {CONTEXT1}: "
        f"clear_args and args cannot be both set at the same time"
    )

    return command_builder_dict, error_message


@case(tags=[FAILED_TAG])
def case_command_builder_from_dict_fail_on_both_clear_args_and_add_args():
    command_builder_dict = {
        HELP: COMMAND_HELP_STRING1,
        CONTEXT1: {ADD_ARGS: [ARG1, ARG2], CLEAR_ARGS: True},
    }
    error_message = (
        f"Inconsistency in {COMMAND1} context specification for {CONTEXT1}: "
        f"clear_args and add_args cannot be both set at the same time"
    )

    return command_builder_dict, error_message


@case(tags=[FAILED_TAG])
def case_command_builder_from_dict_fail_on_both_args_and_add_args():
    command_builder_dict = {
        HELP: COMMAND_HELP_STRING1,
        CONTEXT1: {ARGS: [ARG1, ARG2], ADD_ARGS: [ARG3, ARG4]},
    }
    error_message = (
        f"Inconsistency in {COMMAND1} context specification for {CONTEXT1}: "
        f"args and add_args cannot be both set at the same time"
    )

    return command_builder_dict, error_message


@parametrize_with_cases(
    argnames=["command_builder_dict", "error_message"],
    cases=THIS_MODULE,
    has_tag=FAILED_TAG,
)
def test_command_builder_from_dict_failed(command_builder_dict, error_message):
    with pytest.raises(InconsistentConfiguration, match=f"^{error_message}$"):
        CommandBuilder.from_dict(
            command_name=COMMAND1, builder_setups=command_builder_dict
        )
