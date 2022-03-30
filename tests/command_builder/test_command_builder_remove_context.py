from statue.command_builder import CommandBuilder, ContextSpecification
from statue.context import Context
from tests.constants import (
    ARG1,
    ARG2,
    ARG3,
    COMMAND1,
    COMMAND_HELP_STRING1,
    CONTEXT1,
    CONTEXT2,
    CONTEXT3,
    CONTEXT4,
    CONTEXT5,
    CONTEXT6,
    CONTEXT7,
    CONTEXT_HELP_STRING2,
    CONTEXT_HELP_STRING4,
    CONTEXT_HELP_STRING6,
    CONTEXT_HELP_STRING7,
)


def test_command_builder_remove_required_context_by_name():
    context = Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2)
    command_builder = CommandBuilder(
        name=COMMAND1,
        help=COMMAND_HELP_STRING1,
        required_contexts=[CONTEXT1, CONTEXT2],
        allowed_contexts=[CONTEXT3, CONTEXT4],
        contexts_specifications={
            CONTEXT5: ContextSpecification(args=[ARG1]),
            CONTEXT6: ContextSpecification(args=[ARG2, ARG3]),
        },
    )

    command_builder.remove_context(context)

    assert command_builder.required_contexts == [CONTEXT1]
    assert command_builder.allowed_contexts == [CONTEXT3, CONTEXT4]
    assert command_builder.specified_contexts == [CONTEXT5, CONTEXT6]


def test_command_builder_remove_required_context_by_alias():
    context = Context(name=CONTEXT7, help=CONTEXT_HELP_STRING7, aliases=[CONTEXT2])
    command_builder = CommandBuilder(
        name=COMMAND1,
        help=COMMAND_HELP_STRING1,
        required_contexts=[CONTEXT1, CONTEXT2],
        allowed_contexts=[CONTEXT3, CONTEXT4],
        contexts_specifications={
            CONTEXT5: ContextSpecification(args=[ARG1]),
            CONTEXT6: ContextSpecification(args=[ARG2, ARG3]),
        },
    )

    command_builder.remove_context(context)

    assert command_builder.required_contexts == [CONTEXT1]
    assert command_builder.allowed_contexts == [CONTEXT3, CONTEXT4]
    assert command_builder.specified_contexts == [CONTEXT5, CONTEXT6]


def test_command_builder_remove_allowed_context_by_name():
    context = Context(name=CONTEXT4, help=CONTEXT_HELP_STRING4)
    command_builder = CommandBuilder(
        name=COMMAND1,
        help=COMMAND_HELP_STRING1,
        required_contexts=[CONTEXT1, CONTEXT2],
        allowed_contexts=[CONTEXT3, CONTEXT4],
        contexts_specifications={
            CONTEXT5: ContextSpecification(args=[ARG1]),
            CONTEXT6: ContextSpecification(args=[ARG2, ARG3]),
        },
    )

    command_builder.remove_context(context)

    assert command_builder.required_contexts == [CONTEXT1, CONTEXT2]
    assert command_builder.allowed_contexts == [CONTEXT3]
    assert command_builder.specified_contexts == [CONTEXT5, CONTEXT6]


def test_command_builder_remove_allowed_context_by_alias():
    context = Context(name=CONTEXT7, help=CONTEXT_HELP_STRING7, aliases=[CONTEXT4])
    command_builder = CommandBuilder(
        name=COMMAND1,
        help=COMMAND_HELP_STRING1,
        required_contexts=[CONTEXT1, CONTEXT2],
        allowed_contexts=[CONTEXT3, CONTEXT4],
        contexts_specifications={
            CONTEXT5: ContextSpecification(args=[ARG1]),
            CONTEXT6: ContextSpecification(args=[ARG2, ARG3]),
        },
    )

    command_builder.remove_context(context)

    assert command_builder.required_contexts == [CONTEXT1, CONTEXT2]
    assert command_builder.allowed_contexts == [CONTEXT3]
    assert command_builder.specified_contexts == [CONTEXT5, CONTEXT6]


def test_command_builder_remove_specified_context_by_name():
    context = Context(name=CONTEXT6, help=CONTEXT_HELP_STRING6)
    command_builder = CommandBuilder(
        name=COMMAND1,
        help=COMMAND_HELP_STRING1,
        required_contexts=[CONTEXT1, CONTEXT2],
        allowed_contexts=[CONTEXT3, CONTEXT4],
        contexts_specifications={
            CONTEXT5: ContextSpecification(args=[ARG1]),
            CONTEXT6: ContextSpecification(args=[ARG2, ARG3]),
        },
    )

    command_builder.remove_context(context)

    assert command_builder.required_contexts == [CONTEXT1, CONTEXT2]
    assert command_builder.allowed_contexts == [CONTEXT3, CONTEXT4]
    assert command_builder.specified_contexts == [CONTEXT5]


def test_command_builder_remove_specified_context_by_alias():
    context = Context(name=CONTEXT7, help=CONTEXT_HELP_STRING7, aliases=[CONTEXT6])
    command_builder = CommandBuilder(
        name=COMMAND1,
        help=COMMAND_HELP_STRING1,
        required_contexts=[CONTEXT1, CONTEXT2],
        allowed_contexts=[CONTEXT3, CONTEXT4],
        contexts_specifications={
            CONTEXT5: ContextSpecification(args=[ARG1]),
            CONTEXT6: ContextSpecification(args=[ARG2, ARG3]),
        },
    )

    command_builder.remove_context(context)

    assert command_builder.required_contexts == [CONTEXT1, CONTEXT2]
    assert command_builder.allowed_contexts == [CONTEXT3, CONTEXT4]
    assert command_builder.specified_contexts == [CONTEXT5]
