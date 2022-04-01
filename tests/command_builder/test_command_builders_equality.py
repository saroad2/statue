from pytest_cases import THIS_MODULE, case, parametrize_with_cases

from statue.command_builder import CommandBuilder, ContextSpecification
from tests.constants import (
    ARG1,
    ARG2,
    COMMAND1,
    COMMAND2,
    COMMAND_HELP_STRING1,
    COMMAND_HELP_STRING2,
    CONTEXT1,
    CONTEXT2,
)
from tests.util import dummy_version

EQUAL_TAG = "equal"
NOT_EQUAL_TAG = "not_equal"


# Equal cases


@case(tags=[EQUAL_TAG])
def case_equal_simple():
    command_builder1 = CommandBuilder(name=COMMAND1, help=COMMAND_HELP_STRING1)
    command_builder2 = CommandBuilder(name=COMMAND1, help=COMMAND_HELP_STRING1)
    return command_builder1, command_builder2


@case(tags=[EQUAL_TAG])
def case_equal_with_default_args():
    command_builder1 = CommandBuilder(
        name=COMMAND1, help=COMMAND_HELP_STRING1, default_args=[ARG1, ARG2]
    )
    command_builder2 = CommandBuilder(
        name=COMMAND1, help=COMMAND_HELP_STRING1, default_args=[ARG1, ARG2]
    )
    return command_builder1, command_builder2


@case(tags=[EQUAL_TAG])
def case_equal_with_version():
    version = dummy_version()
    command_builder1 = CommandBuilder(
        name=COMMAND1, help=COMMAND_HELP_STRING1, version=version
    )
    command_builder2 = CommandBuilder(
        name=COMMAND1, help=COMMAND_HELP_STRING1, version=version
    )
    return command_builder1, command_builder2


@case(tags=[EQUAL_TAG])
def case_equal_with_required_contexts():
    command_builder1 = CommandBuilder(
        name=COMMAND1, help=COMMAND_HELP_STRING1, required_contexts=[CONTEXT1, CONTEXT2]
    )
    command_builder2 = CommandBuilder(
        name=COMMAND1, help=COMMAND_HELP_STRING1, required_contexts=[CONTEXT1, CONTEXT2]
    )
    return command_builder1, command_builder2


@case(tags=[EQUAL_TAG])
def case_equal_with_allowed_contexts():
    command_builder1 = CommandBuilder(
        name=COMMAND1, help=COMMAND_HELP_STRING1, allowed_contexts=[CONTEXT1, CONTEXT2]
    )
    command_builder2 = CommandBuilder(
        name=COMMAND1, help=COMMAND_HELP_STRING1, allowed_contexts=[CONTEXT1, CONTEXT2]
    )
    return command_builder1, command_builder2


@case(tags=[EQUAL_TAG])
def case_equal_with_contexts_specifications():
    command_builder1 = CommandBuilder(
        name=CONTEXT1,
        help=COMMAND_HELP_STRING1,
        contexts_specifications={CONTEXT1: ContextSpecification(add_args=[ARG1])},
    )
    command_builder2 = CommandBuilder(
        name=CONTEXT1,
        help=COMMAND_HELP_STRING1,
        contexts_specifications={CONTEXT1: ContextSpecification(add_args=[ARG1])},
    )
    return command_builder1, command_builder2


# Not equal cases


@case(tags=[NOT_EQUAL_TAG])
def case_not_equal_different_name():
    command_builder1 = CommandBuilder(name=COMMAND1, help=COMMAND_HELP_STRING1)
    command_builder2 = CommandBuilder(name=COMMAND2, help=COMMAND_HELP_STRING1)
    return command_builder1, command_builder2


@case(tags=[NOT_EQUAL_TAG])
def case_not_equal_different_help():
    command_builder1 = CommandBuilder(name=COMMAND1, help=COMMAND_HELP_STRING1)
    command_builder2 = CommandBuilder(name=COMMAND1, help=COMMAND_HELP_STRING2)
    return command_builder1, command_builder2


@case(tags=[NOT_EQUAL_TAG])
def case_not_equal_different_version():
    version1, version2 = dummy_version(), dummy_version()
    command_builder1 = CommandBuilder(
        name=COMMAND1, help=COMMAND_HELP_STRING1, version=version1
    )
    command_builder2 = CommandBuilder(
        name=COMMAND1, help=COMMAND_HELP_STRING1, version=version2
    )
    return command_builder1, command_builder2


@case(tags=[NOT_EQUAL_TAG])
def case_not_equal_different_default_args():
    command_builder1 = CommandBuilder(
        name=COMMAND1, help=COMMAND_HELP_STRING1, default_args=[ARG1]
    )
    command_builder2 = CommandBuilder(
        name=COMMAND1, help=COMMAND_HELP_STRING1, default_args=[ARG2]
    )
    return command_builder1, command_builder2


@case(tags=[NOT_EQUAL_TAG])
def case_not_equal_different_allowed_contexts():
    command_builder1 = CommandBuilder(
        name=COMMAND1, help=COMMAND_HELP_STRING1, allowed_contexts=[CONTEXT1]
    )
    command_builder2 = CommandBuilder(
        name=COMMAND1, help=COMMAND_HELP_STRING2, allowed_contexts=[CONTEXT2]
    )
    return command_builder1, command_builder2


@case(tags=[NOT_EQUAL_TAG])
def case_not_equal_different_required_contexts():
    command_builder1 = CommandBuilder(
        name=COMMAND1, help=COMMAND_HELP_STRING1, required_contexts=[CONTEXT1]
    )
    command_builder2 = CommandBuilder(
        name=COMMAND1, help=COMMAND_HELP_STRING2, required_contexts=[CONTEXT2]
    )
    return command_builder1, command_builder2


@case(tags=[NOT_EQUAL_TAG])
def case_not_equal_with_different_contexts_specifications():
    command_builder1 = CommandBuilder(
        name=COMMAND1,
        help=COMMAND_HELP_STRING1,
        contexts_specifications={CONTEXT1: ContextSpecification(add_args=[ARG1])},
    )
    command_builder2 = CommandBuilder(
        name=CONTEXT1,
        help=COMMAND_HELP_STRING1,
        contexts_specifications={CONTEXT1: ContextSpecification(add_args=[ARG2])},
    )
    return command_builder1, command_builder2


@parametrize_with_cases(
    argnames=["command_builder1", "command_builder2"],
    cases=THIS_MODULE,
    has_tag=EQUAL_TAG,
)
def test_command_builders_equality(
    command_builder1, command_builder2
):  # pylint: disable=superfluous-parens
    assert command_builder1 == command_builder2
    assert not (command_builder1 != command_builder2)


@parametrize_with_cases(
    argnames=["command_builder1", "command_builder2"],
    cases=THIS_MODULE,
    has_tag=NOT_EQUAL_TAG,
)
def test_command_builders_non_equality(
    command_builder1, command_builder2
):  # pylint: disable=superfluous-parens
    assert command_builder1 != command_builder2
    assert not (command_builder1 == command_builder2)
