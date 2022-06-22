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
    assert not command_builder.denied_contexts
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
        "denied_contexts=[], "
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
    assert not command_builder.denied_contexts
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
        "denied_contexts=[], "
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
    assert not command_builder.denied_contexts
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
        "denied_contexts=[], "
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
    assert not command_builder.denied_contexts
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
        "denied_contexts=[], "
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
    assert not command_builder.denied_contexts
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
        "denied_contexts=[], "
        "contexts_specifications={}"
        ")"
    )


def test_command_builder_with_denied_contexts():
    context1, context2 = (
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
        Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2),
    )
    command_builder = CommandBuilder(
        name=COMMAND1,
        help=COMMAND_HELP_STRING1,
        denied_contexts=[context1, context2],
    )

    assert command_builder.name == COMMAND1
    assert command_builder.install_name == COMMAND1
    assert command_builder.help == COMMAND_HELP_STRING1
    assert not command_builder.default_args
    assert command_builder.version is None
    assert not command_builder.required_contexts
    assert not command_builder.allowed_contexts
    assert command_builder.denied_contexts == {context1, context2}
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
        f"denied_contexts=['{CONTEXT1}', '{CONTEXT2}'], "
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
    assert not command_builder.denied_contexts
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
        "denied_contexts=[], "
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
    assert not command_builder.denied_contexts
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
        "denied_contexts=[], "
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


def test_command_builder_set_denied_contexts():
    context1, context2 = (
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
        Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2),
    )
    command_builder = CommandBuilder(name=COMMAND1, help=COMMAND_HELP_STRING1)
    assert not command_builder.denied_contexts

    command_builder.denied_contexts = [context1, context2]

    assert command_builder.denied_contexts == {context1, context2}


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


def test_command_builder_reset_all_available_contexts():
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
    command_builder = CommandBuilder(
        name=COMMAND1,
        help=COMMAND_HELP_STRING1,
        required_contexts=[context1, context2],
        allowed_contexts=[context3, context4],
        contexts_specifications={
            context5: context_specification1,
            context6: context_specification2,
        },
    )

    assert command_builder.available_contexts == {
        context1,
        context2,
        context3,
        context4,
        context5,
        context6,
    }

    command_builder.reset_all_available_contexts()

    assert not command_builder.available_contexts


@pytest.mark.parametrize(
    argnames=["type1", "type2", "error_message"],
    argvalues=[
        (
            "allowed_contexts",
            "denied_contexts",
            "allowed and denied contexts clash "
            rf"\({COMMAND1} -> allowed/denied -> {CONTEXT1}\)",
        ),
        (
            "allowed_contexts",
            "required_contexts",
            "allowed and required contexts clash "
            rf"\({COMMAND1} -> allowed/required -> {CONTEXT1}\)",
        ),
        (
            "denied_contexts",
            "required_contexts",
            "denied and required contexts clash "
            rf"\({COMMAND1} -> denied/required -> {CONTEXT1}\)",
        ),
    ],
)
def test_command_builder_constructor_fail_on_context_in_two_listed_types(
    type1, type2, error_message
):
    context1, context2 = (
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
        Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2),
    )
    with pytest.raises(
        InconsistentConfiguration,
        match=f"^{error_message}$",
    ):
        CommandBuilder(
            name=COMMAND1,
            help=COMMAND_HELP_STRING1,
            **{type1: [context1, context2], type2: [context1]},
        )


@pytest.mark.parametrize(
    argnames=["type1", "type2", "error_message"],
    argvalues=[
        (
            "allowed_contexts",
            "denied_contexts",
            rf"allowed and denied contexts clash \({COMMAND1} -> allowed/denied\)",
        ),
        (
            "allowed_contexts",
            "required_contexts",
            rf"allowed and required contexts clash \({COMMAND1} -> allowed/required\)",
        ),
        (
            "denied_contexts",
            "required_contexts",
            rf"denied and required contexts clash \({COMMAND1} -> denied/required\)",
        ),
    ],
)
def test_command_builder_constructor_fail_on_two_contexts_in_two_listed_types(
    type1, type2, error_message
):
    context1, context2, context3 = (
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
        Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2),
        Context(name=CONTEXT3, help=CONTEXT_HELP_STRING3),
    )
    with pytest.raises(
        InconsistentConfiguration,
        match=f"^{error_message}$",
    ):
        CommandBuilder(
            name=COMMAND1,
            help=COMMAND_HELP_STRING1,
            **{type1: [context1, context2, context3], type2: [context1, context2]},
        )


@pytest.mark.parametrize(
    argnames=["type1", "error_message"],
    argvalues=[
        (
            "allowed_contexts",
            "allowed and specified contexts clash "
            rf"\({COMMAND1} -> allowed/specified -> {CONTEXT1}\)",
        ),
        (
            "denied_contexts",
            "denied and specified contexts clash "
            rf"\({COMMAND1} -> denied/specified -> {CONTEXT1}\)",
        ),
        (
            "required_contexts",
            "required and specified contexts clash "
            rf"\({COMMAND1} -> required/specified -> {CONTEXT1}\)",
        ),
    ],
)
def test_command_builder_constructor_fail_on_context_both_in_list_type_and_specified(
    type1, error_message
):
    context1, context2 = (
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
        Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2),
    )
    with pytest.raises(
        InconsistentConfiguration,
        match=f"^{error_message}$",
    ):
        CommandBuilder(
            name=COMMAND1,
            help=COMMAND_HELP_STRING1,
            contexts_specifications={context1: ContextSpecification(args=[ARG1])},
            **{type1: [context1, context2]},
        )


@pytest.mark.parametrize(
    argnames=["constructor_type", "set_type", "error_message"],
    argvalues=[
        (
            "allowed_contexts",
            "denied_contexts",
            "allowed and denied contexts clash "
            rf"\({COMMAND1} -> allowed/denied -> {CONTEXT1}\)",
        ),
        (
            "denied_contexts",
            "allowed_contexts",
            "allowed and denied contexts clash "
            rf"\({COMMAND1} -> allowed/denied -> {CONTEXT1}\)",
        ),
        (
            "allowed_contexts",
            "required_contexts",
            "allowed and required contexts clash "
            rf"\({COMMAND1} -> allowed/required -> {CONTEXT1}\)",
        ),
        (
            "required_contexts",
            "allowed_contexts",
            "allowed and required contexts clash "
            rf"\({COMMAND1} -> allowed/required -> {CONTEXT1}\)",
        ),
        (
            "required_contexts",
            "denied_contexts",
            "denied and required contexts clash "
            rf"\({COMMAND1} -> denied/required -> {CONTEXT1}\)",
        ),
        (
            "denied_contexts",
            "required_contexts",
            "denied and required contexts clash "
            rf"\({COMMAND1} -> denied/required -> {CONTEXT1}\)",
        ),
    ],
)
def test_command_builder_fail_on_set_list_type_context_fail_on_preoccupied(
    constructor_type, set_type, error_message
):
    context = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    command_builder = CommandBuilder(
        name=COMMAND1, help=COMMAND_HELP_STRING1, **{constructor_type: [context]}
    )

    with pytest.raises(
        InconsistentConfiguration,
        match=f"^{error_message}$",
    ):
        setattr(command_builder, set_type, [context])


@pytest.mark.parametrize(
    argnames=["constructor_type", "error_message"],
    argvalues=[
        (
            "allowed_contexts",
            "allowed and specified contexts clash "
            rf"\({COMMAND1} -> allowed/specified -> {CONTEXT1}\)",
        ),
        (
            "denied_contexts",
            "denied and specified contexts clash "
            rf"\({COMMAND1} -> denied/specified -> {CONTEXT1}\)",
        ),
        (
            "required_contexts",
            "required and specified contexts clash "
            rf"\({COMMAND1} -> required/specified -> {CONTEXT1}\)",
        ),
    ],
)
def test_command_builder_fail_on_set_specified_context_fail_on_preoccupied(
    constructor_type, error_message
):
    context = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    command_builder = CommandBuilder(
        name=COMMAND1, help=COMMAND_HELP_STRING1, **{constructor_type: [context]}
    )

    with pytest.raises(
        InconsistentConfiguration,
        match=f"^{error_message}$",
    ):
        command_builder.contexts_specifications = {
            context: ContextSpecification(clear_args=True)
        }


@pytest.mark.parametrize(
    argnames=["set_type", "error_message"],
    argvalues=[
        (
            "allowed_contexts",
            "allowed and specified contexts clash "
            rf"\({COMMAND1} -> allowed/specified -> {CONTEXT1}\)",
        ),
        (
            "denied_contexts",
            "denied and specified contexts clash "
            rf"\({COMMAND1} -> denied/specified -> {CONTEXT1}\)",
        ),
        (
            "required_contexts",
            "required and specified contexts clash "
            rf"\({COMMAND1} -> required/specified -> {CONTEXT1}\)",
        ),
    ],
)
def test_command_builder_fail_on_set_list_type_fail_on_preoccupied_as_specified(
    set_type, error_message
):
    context = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    command_builder = CommandBuilder(
        name=COMMAND1,
        help=COMMAND_HELP_STRING1,
        contexts_specifications={context: ContextSpecification(clear_args=True)},
    )

    with pytest.raises(
        InconsistentConfiguration,
        match=f"^{error_message}$",
    ):
        setattr(command_builder, set_type, [context])
