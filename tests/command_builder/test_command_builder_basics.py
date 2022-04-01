from statue.command_builder import CommandBuilder, ContextSpecification
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
    command_builder = CommandBuilder(
        name=COMMAND1, help=COMMAND_HELP_STRING1, required_contexts=[CONTEXT1, CONTEXT2]
    )

    assert command_builder.name == COMMAND1
    assert command_builder.install_name == COMMAND1
    assert command_builder.help == COMMAND_HELP_STRING1
    assert not command_builder.default_args
    assert command_builder.version is None
    assert command_builder.required_contexts == [CONTEXT1, CONTEXT2]
    assert not command_builder.allowed_contexts
    assert not command_builder.specified_contexts
    assert command_builder.available_contexts == [CONTEXT1, CONTEXT2]
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
    command_builder = CommandBuilder(
        name=COMMAND1, help=COMMAND_HELP_STRING1, allowed_contexts=[CONTEXT1, CONTEXT2]
    )

    assert command_builder.name == COMMAND1
    assert command_builder.install_name == COMMAND1
    assert command_builder.help == COMMAND_HELP_STRING1
    assert not command_builder.default_args
    assert command_builder.version is None
    assert not command_builder.required_contexts
    assert command_builder.allowed_contexts == [CONTEXT1, CONTEXT2]
    assert not command_builder.specified_contexts
    assert command_builder.available_contexts == [CONTEXT1, CONTEXT2]
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
    command_builder = CommandBuilder(
        name=COMMAND1,
        help=COMMAND_HELP_STRING1,
        contexts_specifications={
            CONTEXT1: context_specification1,
            CONTEXT2: context_specification2,
        },
    )

    assert command_builder.name == COMMAND1
    assert command_builder.install_name == COMMAND1
    assert command_builder.help == COMMAND_HELP_STRING1
    assert not command_builder.default_args
    assert command_builder.version is None
    assert not command_builder.required_contexts
    assert not command_builder.allowed_contexts
    assert command_builder.specified_contexts == [CONTEXT1, CONTEXT2]
    assert command_builder.available_contexts == [CONTEXT1, CONTEXT2]
    assert command_builder.contexts_specifications == {
        CONTEXT1: context_specification1,
        CONTEXT2: context_specification2,
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
        required_contexts=[CONTEXT1, CONTEXT2],
        allowed_contexts=[CONTEXT3, CONTEXT4],
        contexts_specifications={
            CONTEXT5: context_specification1,
            CONTEXT6: context_specification2,
        },
    )

    assert command_builder.name == COMMAND1
    assert command_builder.install_name == f"{COMMAND1}=={version}"
    assert command_builder.help == COMMAND_HELP_STRING1
    assert command_builder.default_args == [ARG1, ARG2]
    assert command_builder.version == version
    assert command_builder.required_contexts == [CONTEXT1, CONTEXT2]
    assert command_builder.allowed_contexts == [CONTEXT3, CONTEXT4]
    assert command_builder.specified_contexts == [CONTEXT5, CONTEXT6]
    assert command_builder.available_contexts == [
        CONTEXT1,
        CONTEXT2,
        CONTEXT3,
        CONTEXT4,
        CONTEXT5,
        CONTEXT6,
    ]
    assert command_builder.contexts_specifications == {
        CONTEXT5: context_specification1,
        CONTEXT6: context_specification2,
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
