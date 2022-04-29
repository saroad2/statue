from collections import OrderedDict

import mock
import pytest

from statue.config.contexts_repository import ContextsRepository
from statue.context import Context
from statue.exceptions import InconsistentConfiguration, UnknownContext
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

    assert len(contexts_repository) == 0
    assert not contexts_repository.occupied_names


def test_contexts_repository_with_one_simple_context():
    context = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    contexts_repository = ContextsRepository(context)

    assert len(contexts_repository) == 1
    assert contexts_repository[CONTEXT1] == context
    assert CONTEXT1 in contexts_repository
    assert CONTEXT2 not in contexts_repository
    assert contexts_repository.occupied_names == [CONTEXT1]


def test_contexts_repository_with_three_simple_context():
    context1 = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    context2 = Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2)
    context3 = Context(name=CONTEXT3, help=CONTEXT_HELP_STRING3)
    contexts_repository = ContextsRepository(context1, context2, context3)

    assert len(contexts_repository) == 3
    assert contexts_repository[CONTEXT1] == context1
    assert contexts_repository[CONTEXT2] == context2
    assert contexts_repository[CONTEXT3] == context3
    assert CONTEXT1 in contexts_repository
    assert CONTEXT2 in contexts_repository
    assert CONTEXT3 in contexts_repository
    assert CONTEXT4 not in contexts_repository
    assert contexts_repository.occupied_names == [CONTEXT1, CONTEXT2, CONTEXT3]


def test_contexts_repository_with_one_context_with_aliases():
    context = Context(
        name=CONTEXT1, help=CONTEXT_HELP_STRING1, aliases=[CONTEXT2, CONTEXT3]
    )
    contexts_repository = ContextsRepository(context)

    assert len(contexts_repository) == 1
    assert contexts_repository[CONTEXT1] == context
    assert contexts_repository[CONTEXT2] == context
    assert contexts_repository[CONTEXT3] == context
    assert CONTEXT1 in contexts_repository
    assert CONTEXT2 in contexts_repository
    assert CONTEXT3 in contexts_repository
    assert CONTEXT4 not in contexts_repository
    assert contexts_repository.occupied_names == [CONTEXT1, CONTEXT2, CONTEXT3]


def test_contexts_repository_with_one_context_with_parent():
    parent = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    context = Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2, parent=parent)
    contexts_repository = ContextsRepository(context, parent)

    assert len(contexts_repository) == 2
    assert contexts_repository[CONTEXT1] == parent
    assert contexts_repository[CONTEXT2] == context

    assert CONTEXT1 in contexts_repository
    assert CONTEXT2 in contexts_repository
    assert CONTEXT3 not in contexts_repository
    assert contexts_repository.occupied_names == [CONTEXT1, CONTEXT2]


def test_contexts_repository_with_multiple_contexts():
    parent = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    context1 = Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2, parent=parent)
    parent2 = Context(name=CONTEXT3, help=CONTEXT_HELP_STRING3)
    context2 = Context(name=CONTEXT4, help=CONTEXT_HELP_STRING4, parent=parent2)
    context3 = Context(name=CONTEXT5, help=CONTEXT_HELP_STRING5, parent=parent2)
    contexts_repository = ContextsRepository(
        parent, context1, context2, parent2, context3
    )

    assert len(contexts_repository) == 5
    assert contexts_repository[CONTEXT1] == parent
    assert contexts_repository[CONTEXT2] == context1
    assert contexts_repository[CONTEXT3] == parent2
    assert contexts_repository[CONTEXT4] == context2
    assert contexts_repository[CONTEXT5] == context3
    assert CONTEXT1 in contexts_repository
    assert CONTEXT2 in contexts_repository
    assert CONTEXT3 in contexts_repository
    assert CONTEXT4 in contexts_repository
    assert CONTEXT5 in contexts_repository
    assert contexts_repository.occupied_names == [
        CONTEXT1,
        CONTEXT2,
        CONTEXT3,
        CONTEXT4,
        CONTEXT5,
    ]


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

    assert len(contexts_repository) == 0
    assert CONTEXT1 not in contexts_repository
    assert not contexts_repository.occupied_names


def test_contexts_repository_add_contexts():
    context1 = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    context2 = Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2)
    context3 = Context(name=CONTEXT3, help=CONTEXT_HELP_STRING3)
    context4 = Context(name=CONTEXT4, help=CONTEXT_HELP_STRING4)

    contexts_repository = ContextsRepository(context1, context2)
    contexts_repository.add_contexts(context3, context4)

    assert len(contexts_repository) == 4

    assert contexts_repository[CONTEXT1] == context1
    assert contexts_repository[CONTEXT2] == context2
    assert contexts_repository[CONTEXT3] == context3
    assert contexts_repository[CONTEXT4] == context4
    assert CONTEXT1 in contexts_repository
    assert CONTEXT2 in contexts_repository
    assert CONTEXT3 in contexts_repository
    assert CONTEXT4 in contexts_repository
    assert contexts_repository.occupied_names == [
        CONTEXT1,
        CONTEXT2,
        CONTEXT3,
        CONTEXT4,
    ]


def test_contexts_repository_iterate():
    context1 = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    context2 = Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2)
    context3 = Context(name=CONTEXT3, help=CONTEXT_HELP_STRING3)
    contexts_repository = ContextsRepository(context1, context2, context3)

    assert list(contexts_repository) == [context1, context2, context3]


def test_contexts_repository_remove_context():
    context1 = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    context2 = Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2)
    context3 = Context(name=CONTEXT3, help=CONTEXT_HELP_STRING3)
    contexts_repository = ContextsRepository(context1, context2, context3)
    contexts_repository.remove_context(context2)

    assert contexts_repository[CONTEXT1] == context1
    assert contexts_repository[CONTEXT3] == context3
    assert CONTEXT1 in contexts_repository
    assert CONTEXT2 not in contexts_repository
    assert CONTEXT3 in contexts_repository
    assert contexts_repository.occupied_names == [CONTEXT1, CONTEXT3]


def test_contexts_repository_as_dict():
    context1, context2, context3 = (mock.Mock(), mock.Mock(), mock.Mock())
    context1.name, context2.name, context3.name = CONTEXT1, CONTEXT2, CONTEXT3

    contexts_repository = ContextsRepository(context1, context3, context2)
    contexts_repository_dict = contexts_repository.as_dict()

    assert isinstance(contexts_repository_dict, OrderedDict)
    assert list(contexts_repository_dict.keys()) == [CONTEXT1, CONTEXT2, CONTEXT3]
    assert contexts_repository_dict[CONTEXT1] == context1.as_dict.return_value
    assert contexts_repository_dict[CONTEXT2] == context2.as_dict.return_value
    assert contexts_repository_dict[CONTEXT3] == context3.as_dict.return_value


def test_contexts_repository_fail_getting_unknown_context():
    context1 = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    context2 = Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2)

    contexts_repository = ContextsRepository(context1, context2)

    with pytest.raises(
        UnknownContext, match=f'^Could not find context named "{CONTEXT3}"$'
    ):
        contexts_repository[CONTEXT3]  # pylint: disable=pointless-statement


def test_contexts_repository_fail_on_adding_context_with_existing_name():
    contexts_repository = ContextsRepository(
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    )

    with pytest.raises(
        InconsistentConfiguration,
        match=rf"^context name or alias has been defined twice \({CONTEXT1}\)$",
    ):
        contexts_repository.add_contexts(
            Context(name=CONTEXT1, help=CONTEXT_HELP_STRING2)
        )


def test_contexts_repository_fail_on_adding_context_with_existing_alias():
    contexts_repository = ContextsRepository(
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    )

    with pytest.raises(
        InconsistentConfiguration,
        match=rf"^context name or alias has been defined twice \({CONTEXT1}\)$",
    ):
        contexts_repository.add_contexts(
            Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2, aliases=[CONTEXT1])
        )


def test_contexts_repository_fail_on_adding_two_contexts_with_the_same_name():
    context = Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2)
    contexts_repository = ContextsRepository(context)

    with pytest.raises(
        InconsistentConfiguration,
        match=rf"^context name or alias has been defined twice \({CONTEXT1}\)$",
    ):
        contexts_repository.add_contexts(
            Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
            Context(name=CONTEXT1, help=CONTEXT_HELP_STRING3),
        )

    assert len(contexts_repository) == 1
    assert contexts_repository[CONTEXT2] == context
