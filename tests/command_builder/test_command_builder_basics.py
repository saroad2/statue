import pytest

from statue.command_builder import CommandBuilder
from statue.context import Context
from statue.context_specification import ContextSpecification
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
    CONTEXT_HELP_STRING1,
    CONTEXT_HELP_STRING2,
    CONTEXT_HELP_STRING3,
    CONTEXT_HELP_STRING4,
    CONTEXT_HELP_STRING5,
    CONTEXT_HELP_STRING6,
)
from tests.util import dummy_version


def test_command_builder_empty_constructor():
    command_builder = CommandBuilder(name=COMMAND1, help=COMMAND_HELP_STRING1)

    assert command_builder.name == COMMAND1
    assert command_builder.install_name == COMMAND1
    assert command_builder.help == COMMAND_HELP_STRING1
    assert not command_builder.default_args
    assert command_builder.version is None
    assert not command_builder.required_contexts
    assert not command_builder.allowed_contexts
    assert not command_builder.specified_contexts
    assert not command_builder.available_contexts
    assert command_builder.contexts_specifications == {}
    assert str(command_builder) == (
        "CommandBuilder("
        f"name={COMMAND1}, "
        f"help={COMMAND_HELP_STRING1}, "
        "default_args=[], "
        "version=None, "
        "required_contexts=[], "
        "allowed_contexts=[], "
        "contexts_specifications={}"
        ")"
    )


def test_command_builder_with_version():
    version = dummy_version()
    command_builder = CommandBuilder(
        name=COMMAND1, help=COMMAND_HELP_STRING1, version=version
    )

    assert command_builder.name == COMMAND1
    assert command_builder.install_name == f"{COMMAND1}=={version}"
    assert command_builder.help == COMMAND_HELP_STRING1
    assert not command_builder.default_args
    assert command_builder.version == version
    assert not command_builder.required_contexts
    assert not command_builder.allowed_contexts
    assert not command_builder.specified_contexts
    assert not command_builder.available_contexts
    assert command_builder.contexts_specifications == {}
    assert str(command_builder) == (
        "CommandBuilder("
        f"name={COMMAND1}, "
        f"help={COMMAND_HELP_STRING1}, "
        "default_args=[], "
        f"version={version}, "
        "required_contexts=[], "
        "allowed_contexts=[], "
        "contexts_specifications={}"
        ")"
    )


def test_command_builder_with_default_args():
    command_builder = CommandBuilder(
        name=COMMAND1, help=COMMAND_HELP_STRING1, default_args=[ARG1, ARG2]
    )

    assert command_builder.name == COMMAND1
    assert command_builder.install_name == COMMAND1
    assert command_builder.help == COMMAND_HELP_STRING1
    assert command_builder.default_args == [ARG1, ARG2]
    assert command_builder.version is None
    assert not command_builder.required_contexts
    assert not command_builder.allowed_contexts
    assert not command_builder.specified_contexts
    assert not command_builder.available_contexts
    assert command_builder.contexts_specifications == {}
    assert str(command_builder) == (
        "CommandBuilder("
        f"name={COMMAND1}, "
        f"help={COMMAND_HELP_STRING1}, "
        f"default_args=['{ARG1}', '{ARG2}'], "
        "version=None, "
        "required_contexts=[], "
        "allowed_contexts=[], "
        "contexts_specifications={}"
        ")"
    )


def test_command_builder_with_required_contexts():
    context1, context2 = (
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
        Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2),
    )
    command_builder = CommandBuilder(
        name=COMMAND1,
        help=COMMAND_HELP_STRING1,
        required_contexts=[context1, context2],
    )

    assert command_builder.name == COMMAND1
    assert command_builder.install_name == COMMAND1
    assert command_builder.help == COMMAND_HELP_STRING1
    assert not command_builder.default_args
    assert command_builder.version is None
    assert command_builder.required_contexts == {context1, context2}
    assert not command_builder.allowed_contexts
    assert not command_builder.specified_contexts
    assert command_builder.available_contexts == {context1, context2}
    assert command_builder.contexts_specifications == {}
    assert str(command_builder) == (
        "CommandBuilder("
        f"name={COMMAND1}, "
        f"help={COMMAND_HELP_STRING1}, "
        "default_args=[], "
        "version=None, "
        f"required_contexts=['{CONTEXT1}', '{CONTEXT2}'], "
        "allowed_contexts=[], "
        "contexts_specifications={}"
        ")"
    )


def test_command_builder_with_allowed_contexts():
    context1, context2 = (
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
        Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2),
    )
    command_builder = CommandBuilder(
        name=COMMAND1,
        help=COMMAND_HELP_STRING1,
        allowed_contexts=[context1, context2],
    )

    assert command_builder.name == COMMAND1
    assert command_builder.install_name == COMMAND1
    assert command_builder.help == COMMAND_HELP_STRING1
    assert not command_builder.default_args
    assert command_builder.version is None
    assert not command_builder.required_contexts
    assert command_builder.allowed_contexts == {context1, context2}
    assert not command_builder.specified_contexts
    assert command_builder.available_contexts == {context1, context2}
    assert command_builder.contexts_specifications == {}
    assert str(command_builder) == (
        "CommandBuilder("
        f"name={COMMAND1}, "
        f"help={COMMAND_HELP_STRING1}, "
        "default_args=[], "
        "version=None, "
        "required_contexts=[], "
        f"allowed_contexts=['{CONTEXT1}', '{CONTEXT2}'], "
        "contexts_specifications={}"
        ")"
    )


def test_command_builder_with_specified_contexts():
    context_specification1, context_specification2 = (
        ContextSpecification(args=[ARG1]),
        ContextSpecification(add_args=[ARG2]),
    )
    context1, context2 = (
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
        Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2),
    )
    command_builder = CommandBuilder(
        name=COMMAND1,
        help=COMMAND_HELP_STRING1,
        contexts_specifications={
            context1: context_specification1,
            context2: context_specification2,
        },
    )

    assert command_builder.name == COMMAND1
    assert command_builder.install_name == COMMAND1
    assert command_builder.help == COMMAND_HELP_STRING1
    assert not command_builder.default_args
    assert command_builder.version is None
    assert not command_builder.required_contexts
    assert not command_builder.allowed_contexts
    assert command_builder.specified_contexts == {context1, context2}
    assert command_builder.available_contexts == {context1, context2}
    assert command_builder.contexts_specifications == {
        context1: context_specification1,
        context2: context_specification2,
    }
    assert str(command_builder) == (
        "CommandBuilder("
        f"name={COMMAND1}, "
        f"help={COMMAND_HELP_STRING1}, "
        "default_args=[], "
        "version=None, "
        "required_contexts=[], "
        "allowed_contexts=[], "
        "contexts_specifications={"
        f"'{CONTEXT1}': {str(context_specification1)}, "
        f"'{CONTEXT2}': {str(context_specification2)}"
        "}"
        ")"
    )


def test_command_builder_with_all_fields():
    context1, context2, context3, context4, context5, context6 = (
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
        Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2),
        Context(name=CONTEXT3, help=CONTEXT_HELP_STRING3),
        Context(name=CONTEXT4, help=CONTEXT_HELP_STRING4),
        Context(name=CONTEXT5, help=CONTEXT_HELP_STRING5),
        Context(name=CONTEXT6, help=CONTEXT_HELP_STRING6),
    )
    context_specification1, context_specification2 = (
        ContextSpecification(args=[ARG3]),
        ContextSpecification(add_args=[ARG4]),
    )
    version = dummy_version()
    command_builder = CommandBuilder(
        name=COMMAND1,
        help=COMMAND_HELP_STRING1,
        default_args=[ARG1, ARG2],
        version=version,
        required_contexts=[context1, context2],
        allowed_contexts=[context3, context4],
        contexts_specifications={
            context5: context_specification1,
            context6: context_specification2,
        },
    )

    assert command_builder.name == COMMAND1
    assert command_builder.install_name == f"{COMMAND1}=={version}"
    assert command_builder.help == COMMAND_HELP_STRING1
    assert command_builder.default_args == [ARG1, ARG2]
    assert command_builder.version == version
    assert command_builder.required_contexts == {context1, context2}
    assert command_builder.allowed_contexts == {context3, context4}
    assert command_builder.specified_contexts == {context5, context6}
    assert command_builder.available_contexts == {
        context1,
        context2,
        context3,
        context4,
        context5,
        context6,
    }
    assert command_builder.contexts_specifications == {
        context5: context_specification1,
        context6: context_specification2,
    }
    assert str(command_builder) == (
        "CommandBuilder("
        f"name={COMMAND1}, "
        f"help={COMMAND_HELP_STRING1}, "
        f"default_args=['{ARG1}', '{ARG2}'], "
        f"version={version}, "
        f"required_contexts=['{CONTEXT1}', '{CONTEXT2}'], "
        f"allowed_contexts=['{CONTEXT3}', '{CONTEXT4}'], "
        "contexts_specifications={"
        f"'{CONTEXT5}': {str(context_specification1)}, "
        f"'{CONTEXT6}': {str(context_specification2)}"
        "}"
        ")"
    )


def test_command_builder_set_required_contexts():
    context1, context2 = (
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
        Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2),
    )
    command_builder = CommandBuilder(name=COMMAND1, help=COMMAND_HELP_STRING1)
    assert not command_builder.required_contexts

    command_builder.required_contexts = [context1, context2]

    assert command_builder.required_contexts == {context1, context2}


def test_command_builder_set_allowed_contexts():
    context1, context2 = (
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
        Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2),
    )
    command_builder = CommandBuilder(name=COMMAND1, help=COMMAND_HELP_STRING1)
    assert not command_builder.allowed_contexts

    command_builder.allowed_contexts = [context1, context2]

    assert command_builder.allowed_contexts == {context1, context2}


def test_command_builder_set_contexts_specification():
    context1, context2 = (
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
        Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2),
    )
    contexts_specifications = {
        context1: ContextSpecification(add_args=[ARG1]),
        context2: ContextSpecification(clear_args=True),
    }
    command_builder = CommandBuilder(name=COMMAND1, help=COMMAND_HELP_STRING1)
    assert not command_builder.contexts_specifications

    command_builder.contexts_specifications = contexts_specifications

    assert command_builder.contexts_specifications == contexts_specifications


def test_command_builder_constructor_fail_on_one_context_both_allowed_and_required():
    context1, context2 = (
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
        Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2),
    )
    with pytest.raises(
        InconsistentConfiguration,
        match=(
            "^allowed and required contexts clash "
            rf"\({COMMAND1} -> allowed/required -> {CONTEXT1}\)$"
        ),
    ):
        CommandBuilder(
            name=COMMAND1,
            help=COMMAND_HELP_STRING1,
            allowed_contexts=[context1, context2],
            required_contexts=[context1],
        )


def test_command_builder_constructor_fail_with_two_contexts_both_allowed_and_required():
    context1, context2, context3 = (
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
        Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2),
        Context(name=CONTEXT3, help=CONTEXT_HELP_STRING3),
    )
    with pytest.raises(
        InconsistentConfiguration,
        match=(
            "^allowed and required contexts clash "
            rf"\({COMMAND1} -> allowed/required\)$"
        ),
    ):
        CommandBuilder(
            name=COMMAND1,
            help=COMMAND_HELP_STRING1,
            allowed_contexts=[context1, context2, context3],
            required_contexts=[context1, context2],
        )


def test_command_builder_constructor_fail_on_one_context_both_allowed_and_specified():
    context1, context2 = (
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
        Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2),
    )
    with pytest.raises(
        InconsistentConfiguration,
        match=(
            "^allowed and specified contexts clash "
            rf"\({COMMAND1} -> allowed/specified -> {CONTEXT1}\)$"
        ),
    ):
        CommandBuilder(
            name=COMMAND1,
            help=COMMAND_HELP_STRING1,
            allowed_contexts=[context1, context2],
            contexts_specifications={context1: ContextSpecification(args=[ARG1])},
        )


def test_command_builder_constructor_fail_on_two_contexts_both_allowed_and_specified():
    context1, context2, context3 = (
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
        Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2),
        Context(name=CONTEXT3, help=CONTEXT_HELP_STRING3),
    )
    with pytest.raises(
        InconsistentConfiguration,
        match=(
            "^allowed and specified contexts clash "
            rf"\({COMMAND1} -> allowed/specified\)$"
        ),
    ):
        CommandBuilder(
            name=COMMAND1,
            help=COMMAND_HELP_STRING1,
            allowed_contexts=[context1, context2, context3],
            contexts_specifications={
                context1: ContextSpecification(args=[ARG1]),
                context2: ContextSpecification(args=[ARG2]),
            },
        )


def test_command_builder_constructor_fail_on_one_context_both_required_and_specified():
    context1, context2 = (
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
        Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2),
    )
    with pytest.raises(
        InconsistentConfiguration,
        match=(
            "^required and specified contexts clash "
            rf"\({COMMAND1} -> required/specified -> {CONTEXT1}\)$"
        ),
    ):
        CommandBuilder(
            name=COMMAND1,
            help=COMMAND_HELP_STRING1,
            required_contexts=[context1, context2],
            contexts_specifications={context1: ContextSpecification(args=[ARG1])},
        )


def test_command_builder_constructor_fail_on_two_contexts_both_required_and_specified():
    context1, context2, context3 = (
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
        Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2),
        Context(name=CONTEXT3, help=CONTEXT_HELP_STRING3),
    )
    with pytest.raises(
        InconsistentConfiguration,
        match=(
            "^required and specified contexts clash "
            rf"\({COMMAND1} -> required/specified\)$"
        ),
    ):
        CommandBuilder(
            name=COMMAND1,
            help=COMMAND_HELP_STRING1,
            required_contexts=[context1, context2, context3],
            contexts_specifications={
                context1: ContextSpecification(args=[ARG1]),
                context2: ContextSpecification(args=[ARG2]),
            },
        )


def test_command_builder_fail_on_set_required_context_fail_on_preoccupied():
    context = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    command_builder = CommandBuilder(
        name=COMMAND1, help=COMMAND_HELP_STRING1, allowed_contexts=[context]
    )

    with pytest.raises(
        InconsistentConfiguration,
        match=(
            "^allowed and required contexts clash "
            rf"\({COMMAND1} -> allowed/required -> {CONTEXT1}\)$"
        ),
    ):
        command_builder.required_contexts = [context]


def test_command_builder_fail_on_set_allowed_context_fail_on_preoccupied():
    context = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    command_builder = CommandBuilder(
        name=COMMAND1, help=COMMAND_HELP_STRING1, required_contexts=[context]
    )

    with pytest.raises(
        InconsistentConfiguration,
        match=(
            "^allowed and required contexts clash "
            rf"\({COMMAND1} -> allowed/required -> {CONTEXT1}\)$"
        ),
    ):
        command_builder.allowed_contexts = [context]


def test_command_builder_fail_on_set_specified_context_fail_on_preoccupied():
    context = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    command_builder = CommandBuilder(
        name=COMMAND1, help=COMMAND_HELP_STRING1, required_contexts=[context]
    )

    with pytest.raises(
        InconsistentConfiguration,
        match=(
            "^required and specified contexts clash "
            rf"\({COMMAND1} -> required/specified -> {CONTEXT1}\)$"
        ),
    ):
        command_builder.contexts_specifications = {
            context: ContextSpecification(clear_args=True)
        }
