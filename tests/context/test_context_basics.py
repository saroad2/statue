import pytest

from statue.context import Context
from statue.exceptions import ContextCircularParentingError
from tests.constants import (
    CONTEXT1,
    CONTEXT2,
    CONTEXT3,
    CONTEXT_HELP_STRING1,
    CONTEXT_HELP_STRING2,
    CONTEXT_HELP_STRING3,
)


def test_context_default_constructor():
    context = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)

    assert context.name == CONTEXT1
    assert not context.aliases
    assert context.all_names == [CONTEXT1]
    assert context.help == CONTEXT_HELP_STRING1
    assert context.parent is None
    assert context.parents == []
    assert not context.allowed_by_default
    assert str(context) == (
        "Context("
        f"name='{CONTEXT1}', "
        f"help='{CONTEXT_HELP_STRING1}', "
        "aliases=[], "
        "parent=None, "
        "allowed_by_default=False"
        ")"
    )


def test_context_constructor_with_aliases():
    context = Context(
        name=CONTEXT1, help=CONTEXT_HELP_STRING1, aliases=[CONTEXT2, CONTEXT3]
    )

    assert context.name == CONTEXT1
    assert context.aliases == [CONTEXT2, CONTEXT3]
    assert context.all_names == [CONTEXT1, CONTEXT2, CONTEXT3]
    assert context.help == CONTEXT_HELP_STRING1
    assert context.parent is None
    assert context.parents == []
    assert not context.allowed_by_default
    assert str(context) == (
        "Context("
        f"name='{CONTEXT1}', "
        f"help='{CONTEXT_HELP_STRING1}', "
        f"aliases=['{CONTEXT2}', '{CONTEXT3}'], "
        "parent=None, "
        "allowed_by_default=False"
        ")"
    )


def test_context_constructor_with_parent():
    parent = Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2)
    context = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1, parent=parent)

    assert context.name == CONTEXT1
    assert not context.aliases
    assert context.all_names == [CONTEXT1]
    assert context.help == CONTEXT_HELP_STRING1
    assert context.parent == parent
    assert context.parents == [parent]
    assert not context.allowed_by_default

    parent_str = str(parent)
    assert parent_str == (
        "Context("
        f"name='{CONTEXT2}', "
        f"help='{CONTEXT_HELP_STRING2}', "
        "aliases=[], "
        f"parent=None, "
        "allowed_by_default=False"
        ")"
    )
    assert str(context) == (
        "Context("
        f"name='{CONTEXT1}', "
        f"help='{CONTEXT_HELP_STRING1}', "
        "aliases=[], "
        f"parent={parent_str}, "
        "allowed_by_default=False"
        ")"
    )


def test_context_constructor_with_grandparent():
    grandparent = Context(name=CONTEXT3, help=CONTEXT_HELP_STRING3)
    parent = Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2, parent=grandparent)
    context = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1, parent=parent)

    assert context.name == CONTEXT1
    assert not context.aliases
    assert context.all_names == [CONTEXT1]
    assert context.help == CONTEXT_HELP_STRING1
    assert context.parent == parent
    assert context.parents == [parent, grandparent]
    assert not context.allowed_by_default

    grandparent_str, parent_str = str(grandparent), str(parent)
    assert grandparent_str == (
        "Context("
        f"name='{CONTEXT3}', "
        f"help='{CONTEXT_HELP_STRING3}', "
        "aliases=[], "
        f"parent=None, "
        "allowed_by_default=False"
        ")"
    )
    assert parent_str == (
        "Context("
        f"name='{CONTEXT2}', "
        f"help='{CONTEXT_HELP_STRING2}', "
        "aliases=[], "
        f"parent={grandparent_str}, "
        "allowed_by_default=False"
        ")"
    )
    assert str(context) == (
        "Context("
        f"name='{CONTEXT1}', "
        f"help='{CONTEXT_HELP_STRING1}', "
        "aliases=[], "
        f"parent={parent_str}, "
        "allowed_by_default=False"
        ")"
    )


def test_context_constructor_allowed_by_default():
    context = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1, allowed_by_default=True)

    assert context.name == CONTEXT1
    assert not context.aliases
    assert context.all_names == [CONTEXT1]
    assert context.help == CONTEXT_HELP_STRING1
    assert context.parent is None
    assert context.allowed_by_default
    assert str(context) == (
        "Context("
        f"name='{CONTEXT1}', "
        f"help='{CONTEXT_HELP_STRING1}', "
        "aliases=[], "
        f"parent=None, "
        "allowed_by_default=True"
        ")"
    )


def test_context_clear_aliases():
    context = Context(
        name=CONTEXT1, help=CONTEXT_HELP_STRING1, aliases=[CONTEXT2, CONTEXT3]
    )
    context.clear_aliases()

    assert context.name == CONTEXT1
    assert not context.aliases
    assert context.all_names == [CONTEXT1]
    assert context.help == CONTEXT_HELP_STRING1
    assert context.parent is None
    assert not context.allowed_by_default
    assert str(context) == (
        "Context("
        f"name='{CONTEXT1}', "
        f"help='{CONTEXT_HELP_STRING1}', "
        "aliases=[], "
        f"parent=None, "
        "allowed_by_default=False"
        ")"
    )


def test_context_cannot_set_circular_parenting():
    parent = Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2)
    context = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1, parent=parent)

    with pytest.raises(
        ContextCircularParentingError,
        match=f'^Cannot set circular parenting between "{CONTEXT2}" and "{CONTEXT1}"$',
    ):
        parent.parent = context


def test_context_cannot_set_circular_grandparenting():
    grandparent = Context(name=CONTEXT3, help=CONTEXT_HELP_STRING3)
    parent = Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2, parent=grandparent)
    context = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1, parent=parent)

    with pytest.raises(
        ContextCircularParentingError,
        match=f'^Cannot set circular parenting between "{CONTEXT3}" and "{CONTEXT1}"$',
    ):
        grandparent.parent = context
