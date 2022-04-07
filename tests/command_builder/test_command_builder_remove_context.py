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
    CONTEXT_HELP_STRING1,
    CONTEXT_HELP_STRING2,
    CONTEXT_HELP_STRING3,
    CONTEXT_HELP_STRING4,
    CONTEXT_HELP_STRING5,
    CONTEXT_HELP_STRING6,
)


def test_command_builder_remove_required_context_by_name():
    context1, context2, context3, context4, context5, context6 = (
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
        Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2),
        Context(name=CONTEXT3, help=CONTEXT_HELP_STRING3),
        Context(name=CONTEXT4, help=CONTEXT_HELP_STRING4),
        Context(name=CONTEXT5, help=CONTEXT_HELP_STRING5),
        Context(name=CONTEXT6, help=CONTEXT_HELP_STRING6),
    )
    command_builder = CommandBuilder(
        name=COMMAND1,
        help=COMMAND_HELP_STRING1,
        required_contexts=[context1, context2],
        allowed_contexts=[context3, context4],
        contexts_specifications={
            context5: ContextSpecification(args=[ARG1]),
            context6: ContextSpecification(args=[ARG2, ARG3]),
        },
    )

    command_builder.remove_context(context2)

    assert command_builder.required_contexts == {context1}
    assert command_builder.allowed_contexts == {context3, context4}
    assert command_builder.specified_contexts == {context5, context6}


def test_command_builder_remove_allowed_context_by_name():
    context1, context2, context3, context4, context5, context6 = (
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
        Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2),
        Context(name=CONTEXT3, help=CONTEXT_HELP_STRING3),
        Context(name=CONTEXT4, help=CONTEXT_HELP_STRING4),
        Context(name=CONTEXT5, help=CONTEXT_HELP_STRING5),
        Context(name=CONTEXT6, help=CONTEXT_HELP_STRING6),
    )
    command_builder = CommandBuilder(
        name=COMMAND1,
        help=COMMAND_HELP_STRING1,
        required_contexts=[context1, context2],
        allowed_contexts=[context3, context4],
        contexts_specifications={
            context5: ContextSpecification(args=[ARG1]),
            context6: ContextSpecification(args=[ARG2, ARG3]),
        },
    )

    command_builder.remove_context(context4)

    assert command_builder.required_contexts == {context1, context2}
    assert command_builder.allowed_contexts == {context3}
    assert command_builder.specified_contexts == {context5, context6}


def test_command_builder_remove_specified_context_by_name():
    context1, context2, context3, context4, context5, context6 = (
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
        Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2),
        Context(name=CONTEXT3, help=CONTEXT_HELP_STRING3),
        Context(name=CONTEXT4, help=CONTEXT_HELP_STRING4),
        Context(name=CONTEXT5, help=CONTEXT_HELP_STRING5),
        Context(name=CONTEXT6, help=CONTEXT_HELP_STRING6),
    )
    command_builder = CommandBuilder(
        name=COMMAND1,
        help=COMMAND_HELP_STRING1,
        required_contexts=[context1, context2],
        allowed_contexts=[context3, context4],
        contexts_specifications={
            context5: ContextSpecification(args=[ARG1]),
            context6: ContextSpecification(args=[ARG2, ARG3]),
        },
    )

    command_builder.remove_context(context6)

    assert command_builder.required_contexts == {context1, context2}
    assert command_builder.allowed_contexts == {context3, context4}
    assert command_builder.specified_contexts == {context5}
