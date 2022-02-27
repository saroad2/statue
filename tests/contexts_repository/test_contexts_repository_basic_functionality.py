import pytest

from statue.context import Context
from statue.contexts_repository import ContextsRepository
from statue.exceptions import UnknownContext
from tests.constants import (
    CONTEXT1,
    CONTEXT2,
    CONTEXT3,
    CONTEXT4,
    CONTEXT5,
    CONTEXT_HELP_STRING1,
    CONTEXT_HELP_STRING2,
    CONTEXT_HELP_STRING3,
    CONTEXT_HELP_STRING4,
    CONTEXT_HELP_STRING5,
)


def test_contexts_repository_simple_constructor():
    contexts_repository = ContextsRepository()

    assert contexts_repository.contexts_number == 0


def test_contexts_repository_with_one_simple_context():
    context = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    contexts_repository = ContextsRepository(context)

    assert contexts_repository.contexts_number == 1
    assert contexts_repository.get_context(CONTEXT1) == context
    assert contexts_repository.has_context(CONTEXT1)
    assert not contexts_repository.has_context(CONTEXT2)


def test_contexts_repository_with_three_simple_context():
    context1 = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    context2 = Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2)
    context3 = Context(name=CONTEXT3, help=CONTEXT_HELP_STRING3)
    contexts_repository = ContextsRepository(context1, context2, context3)

    assert contexts_repository.contexts_number == 3
    assert contexts_repository.get_context(CONTEXT1) == context1
    assert contexts_repository.get_context(CONTEXT2) == context2
    assert contexts_repository.get_context(CONTEXT3) == context3
    assert contexts_repository.has_context(CONTEXT1)
    assert contexts_repository.has_context(CONTEXT2)
    assert contexts_repository.has_context(CONTEXT3)
    assert not contexts_repository.has_context(CONTEXT4)


def test_contexts_repository_with_one_context_with_aliases():
    context = Context(
        name=CONTEXT1, help=CONTEXT_HELP_STRING1, aliases=[CONTEXT2, CONTEXT3]
    )
    contexts_repository = ContextsRepository(context)

    assert contexts_repository.contexts_number == 1
    assert contexts_repository.get_context(CONTEXT1) == context
    assert contexts_repository.get_context(CONTEXT2) == context
    assert contexts_repository.get_context(CONTEXT3) == context
    assert contexts_repository.has_context(CONTEXT1)
    assert contexts_repository.has_context(CONTEXT2)
    assert contexts_repository.has_context(CONTEXT3)
    assert not contexts_repository.has_context(CONTEXT4)


def test_contexts_repository_with_one_context_with_parent():
    parent = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    context = Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2, parent=parent)
    contexts_repository = ContextsRepository(context, parent)

    assert contexts_repository.contexts_number == 2
    assert contexts_repository.get_context(CONTEXT1) == parent
    assert contexts_repository.get_context(CONTEXT2) == context

    assert contexts_repository.has_context(CONTEXT1)
    assert contexts_repository.has_context(CONTEXT2)
    assert not contexts_repository.has_context(CONTEXT3)


def test_contexts_repository_with_multiple_contexts():
    parent = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    context1 = Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2, parent=parent)
    parent2 = Context(name=CONTEXT3, help=CONTEXT_HELP_STRING3)
    context2 = Context(name=CONTEXT4, help=CONTEXT_HELP_STRING4, parent=parent2)
    context3 = Context(name=CONTEXT5, help=CONTEXT_HELP_STRING5, parent=parent2)
    contexts_repository = ContextsRepository(
        parent, context1, context2, parent2, context3
    )

    assert contexts_repository.contexts_number == 5
    assert contexts_repository.get_context(CONTEXT1) == parent
    assert contexts_repository.get_context(CONTEXT2) == context1
    assert contexts_repository.get_context(CONTEXT3) == parent2
    assert contexts_repository.get_context(CONTEXT4) == context2
    assert contexts_repository.get_context(CONTEXT5) == context3
    assert contexts_repository.has_context(CONTEXT1)
    assert contexts_repository.has_context(CONTEXT2)
    assert contexts_repository.has_context(CONTEXT3)
    assert contexts_repository.has_context(CONTEXT4)
    assert contexts_repository.has_context(CONTEXT5)


def test_contexts_repository_reset():
    parent = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    context1 = Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2, parent=parent)
    parent2 = Context(name=CONTEXT3, help=CONTEXT_HELP_STRING3)
    context2 = Context(name=CONTEXT4, help=CONTEXT_HELP_STRING4, parent=parent2)
    context3 = Context(name=CONTEXT5, help=CONTEXT_HELP_STRING5, parent=parent2)

    contexts_repository = ContextsRepository(
        parent, context1, context2, parent2, context3
    )
    contexts_repository.reset()

    assert contexts_repository.contexts_number == 0
    assert not contexts_repository.has_context(CONTEXT1)


def test_contexts_repository_add_contexts():
    context1 = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    context2 = Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2)
    context3 = Context(name=CONTEXT3, help=CONTEXT_HELP_STRING3)
    context4 = Context(name=CONTEXT4, help=CONTEXT_HELP_STRING4)

    contexts_repository = ContextsRepository(context1, context2)
    contexts_repository.add_contexts(context3, context4)

    assert contexts_repository.contexts_number == 4

    assert contexts_repository.get_context(CONTEXT1) == context1
    assert contexts_repository.get_context(CONTEXT2) == context2
    assert contexts_repository.get_context(CONTEXT3) == context3
    assert contexts_repository.get_context(CONTEXT4) == context4
    assert contexts_repository.has_context(CONTEXT1)
    assert contexts_repository.has_context(CONTEXT2)
    assert contexts_repository.has_context(CONTEXT3)
    assert contexts_repository.has_context(CONTEXT4)


def test_contexts_repository_iterate():
    context1 = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    context2 = Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2)
    context3 = Context(name=CONTEXT3, help=CONTEXT_HELP_STRING3)
    contexts_repository = ContextsRepository(context1, context2, context3)

    assert list(contexts_repository) == [context1, context2, context3]


def test_contexts_repository_fail_getting_unknown_context():
    context1 = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    context2 = Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2)

    contexts_repository = ContextsRepository(context1, context2)

    with pytest.raises(
        UnknownContext, match=f'^Could not find context named "{CONTEXT3}"$'
    ):
        contexts_repository.get_context(CONTEXT3)
