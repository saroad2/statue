import pytest
from pytest_cases import THIS_MODULE, case, parametrize_with_cases

from statue.command_builder import CommandBuilder, ContextSpecification
from statue.constants import (
    ADD_ARGS,
    ALLOWED_CONTEXTS,
    ARGS,
    CLEAR_ARGS,
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
from tests.util import dummy_version


@case(tags=SUCCESSFUL_TAG)
def case_command_builder_update_from_config_with_nothing():
    version = dummy_version()
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
    update_config = {}
    result_command_builder = CommandBuilder(
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

    return command_builder, update_config, result_command_builder


@case(tags=SUCCESSFUL_TAG)
def case_command_builder_update_from_config_version():
    old_version, new_version = dummy_version(), dummy_version()
    command_builder = CommandBuilder(
        name=COMMAND1, help=COMMAND_HELP_STRING1, version=old_version
    )
    update_config = {VERSION: new_version}
    result_command_builder = CommandBuilder(
        name=COMMAND1, help=COMMAND_HELP_STRING1, version=new_version
    )

    return command_builder, update_config, result_command_builder


@case(tags=SUCCESSFUL_TAG)
def case_command_builder_update_from_config_override_default_args():
    command_builder = CommandBuilder(
        name=COMMAND1, help=COMMAND_HELP_STRING1, default_args=[ARG1, ARG2]
    )
    update_config = {ARGS: [ARG3, ARG4]}
    result_command_builder = CommandBuilder(
        name=COMMAND1, help=COMMAND_HELP_STRING1, default_args=[ARG3, ARG4]
    )

    return command_builder, update_config, result_command_builder


@case(tags=SUCCESSFUL_TAG)
def case_command_builder_update_from_config_from_config_add_default_args():
    command_builder = CommandBuilder(
        name=COMMAND1, help=COMMAND_HELP_STRING1, default_args=[ARG1, ARG2]
    )
    update_config = {ADD_ARGS: [ARG3, ARG4]}
    result_command_builder = CommandBuilder(
        name=COMMAND1, help=COMMAND_HELP_STRING1, default_args=[ARG1, ARG2, ARG3, ARG4]
    )

    return command_builder, update_config, result_command_builder


@case(tags=SUCCESSFUL_TAG)
def case_command_builder_update_from_config_clear_default_args():
    command_builder = CommandBuilder(
        name=COMMAND1, help=COMMAND_HELP_STRING1, default_args=[ARG1, ARG2]
    )
    update_config = {CLEAR_ARGS: True}
    result_command_builder = CommandBuilder(name=COMMAND1, help=COMMAND_HELP_STRING1)

    return command_builder, update_config, result_command_builder


@case(tags=SUCCESSFUL_TAG)
def case_command_builder_update_from_config_from_config_add_required_contexts():
    command_builder = CommandBuilder(
        name=COMMAND1, help=COMMAND_HELP_STRING1, required_contexts=[CONTEXT1, CONTEXT2]
    )
    update_config = {REQUIRED_CONTEXTS: [CONTEXT3, CONTEXT4]}
    result_command_builder = CommandBuilder(
        name=COMMAND1,
        help=COMMAND_HELP_STRING1,
        required_contexts=[CONTEXT1, CONTEXT2, CONTEXT3, CONTEXT4],
    )

    return command_builder, update_config, result_command_builder


@case(tags=SUCCESSFUL_TAG)
def case_command_builder_update_from_config_from_config_add_allowed_contexts():
    command_builder = CommandBuilder(
        name=COMMAND1, help=COMMAND_HELP_STRING1, allowed_contexts=[CONTEXT1, CONTEXT2]
    )
    update_config = {ALLOWED_CONTEXTS: [CONTEXT3, CONTEXT4]}
    result_command_builder = CommandBuilder(
        name=COMMAND1,
        help=COMMAND_HELP_STRING1,
        allowed_contexts=[CONTEXT1, CONTEXT2, CONTEXT3, CONTEXT4],
    )

    return command_builder, update_config, result_command_builder


@case(tags=SUCCESSFUL_TAG)
def case_command_builder_update_from_config_override_context_specification():
    command_builder = CommandBuilder(
        name=COMMAND1,
        help=COMMAND_HELP_STRING1,
        contexts_specifications={CONTEXT1: ContextSpecification(clear_args=True)},
    )
    update_config = {CONTEXT1: {ADD_ARGS: [ARG1, ARG2]}}
    result_command_builder = CommandBuilder(
        name=COMMAND1,
        help=COMMAND_HELP_STRING1,
        contexts_specifications={CONTEXT1: ContextSpecification(add_args=[ARG1, ARG2])},
    )

    return command_builder, update_config, result_command_builder


@case(tags=SUCCESSFUL_TAG)
def case_command_builder_update_from_config_from_config_add_context_specification():
    command_builder = CommandBuilder(
        name=COMMAND1,
        help=COMMAND_HELP_STRING1,
        contexts_specifications={CONTEXT1: ContextSpecification(clear_args=True)},
    )
    update_config = {CONTEXT2: {ADD_ARGS: [ARG1, ARG2]}}
    result_command_builder = CommandBuilder(
        name=COMMAND1,
        help=COMMAND_HELP_STRING1,
        contexts_specifications={
            CONTEXT1: ContextSpecification(clear_args=True),
            CONTEXT2: ContextSpecification(add_args=[ARG1, ARG2]),
        },
    )

    return command_builder, update_config, result_command_builder


@parametrize_with_cases(
    argnames=["command_builder", "update_config", "result_command_builder"],
    cases=THIS_MODULE,
    has_tag=SUCCESSFUL_TAG,
)
def test_command_builder_update_from_config_successfully(
    command_builder, update_config, result_command_builder
):
    command_builder.update_from_config(update_config)
    assert command_builder == result_command_builder


# Failed tests


@case(tags=[FAILED_TAG])
def case_command_builder_update_from_config_fail_on_both_clear_args_and_args():
    command_builder = CommandBuilder(
        name=COMMAND1,
        help=COMMAND_HELP_STRING1,
        contexts_specifications={CONTEXT1: ContextSpecification(clear_args=True)},
    )
    update_config = {CLEAR_ARGS: True, ARGS: [ARG1, ARG2]}
    error_message = (
        f"Inconsistency in {COMMAND1}: "
        f"clear_args and args cannot be both set at the same time"
    )

    return command_builder, update_config, error_message


@case(tags=[FAILED_TAG])
def case_command_builder_update_from_config_fail_on_both_clear_args_and_add_args():
    command_builder = CommandBuilder(
        name=COMMAND1,
        help=COMMAND_HELP_STRING1,
        contexts_specifications={CONTEXT1: ContextSpecification(clear_args=True)},
    )
    update_config = {CLEAR_ARGS: True, ADD_ARGS: [ARG1, ARG2]}
    error_message = (
        f"Inconsistency in {COMMAND1}: "
        f"clear_args and add_args cannot be both set at the same time"
    )

    return command_builder, update_config, error_message


@case(tags=[FAILED_TAG])
def case_command_builder_update_from_config_fail_on_both_args_and_add_args():
    command_builder = CommandBuilder(
        name=COMMAND1,
        help=COMMAND_HELP_STRING1,
        contexts_specifications={CONTEXT1: ContextSpecification(clear_args=True)},
    )
    update_config = {ARGS: [ARG1, ARG2], ADD_ARGS: [ARG3, ARG4]}
    error_message = (
        f"Inconsistency in {COMMAND1}: "
        f"args and add_args cannot be both set at the same time"
    )

    return command_builder, update_config, error_message


@parametrize_with_cases(
    argnames=["command_builder", "update_config", "error_message"],
    cases=THIS_MODULE,
    has_tag=FAILED_TAG,
)
def test_command_builder_update_from_config_failed(
    command_builder, update_config, error_message
):
    with pytest.raises(InconsistentConfiguration, match=f"^{error_message}$"):
        command_builder.update_from_config(update_config)
