from statue.context import Context
from tests.constants import (
    CONTEXT1,
    CONTEXT2,
    CONTEXT3,
    CONTEXT_HELP_STRING1,
    CONTEXT_HELP_STRING2,
)


def test_context_default_constructor():
    context = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)

    assert context.name == CONTEXT1
    assert context.aliases == []
    assert context.all_names == [CONTEXT1]
    assert context.help == CONTEXT_HELP_STRING1
    assert context.parent is None
    assert not context.allowed_by_default


def test_context_constructor_with_aliases():
    context = Context(
        name=CONTEXT1, help=CONTEXT_HELP_STRING1, aliases=[CONTEXT2, CONTEXT3]
    )

    assert context.name == CONTEXT1
    assert context.aliases == [CONTEXT2, CONTEXT3]
    assert context.all_names == [CONTEXT1, CONTEXT2, CONTEXT3]
    assert context.help == CONTEXT_HELP_STRING1
    assert context.parent is None
    assert not context.allowed_by_default


def test_context_constructor_with_parent():
    parent = Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2)
    context = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1, parent=parent)

    assert context.name == CONTEXT1
    assert context.aliases == []
    assert context.all_names == [CONTEXT1]
    assert context.help == CONTEXT_HELP_STRING1
    assert context.parent == parent
    assert not context.allowed_by_default


def test_context_constructor_allowed_by_default():
    context = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1, allowed_by_default=True)

    assert context.name == CONTEXT1
    assert context.aliases == []
    assert context.all_names == [CONTEXT1]
    assert context.help == CONTEXT_HELP_STRING1
    assert context.parent is None
    assert context.allowed_by_default
