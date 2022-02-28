import pytest

from statue.constants import ALIASES, ALLOWED_BY_DEFAULT, HELP, PARENT
from statue.context import Context
from statue.contexts_repository import ContextsRepository
from statue.exceptions import InconsistentConfiguration
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
)


def test_contexts_repository_update_from_empty_config():
    context1 = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    context2 = Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2)
    contexts_repository = ContextsRepository(context1, context2)

    contexts_repository.update_from_config({})

    assert len(contexts_repository) == 2
    assert contexts_repository[CONTEXT1] == context1
    assert contexts_repository[CONTEXT2] == context2


def test_contexts_repository_update_adds_new_simple_context():
    context1 = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    context2 = Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2)
    contexts_repository = ContextsRepository(context1, context2)

    contexts_repository.update_from_config({CONTEXT3: {HELP: CONTEXT_HELP_STRING3}})

    assert len(contexts_repository) == 3
    assert contexts_repository[CONTEXT1] == context1
    assert contexts_repository[CONTEXT2] == context2
    assert contexts_repository[CONTEXT3] == Context(
        name=CONTEXT3, help=CONTEXT_HELP_STRING3
    )


def test_contexts_repository_update_adds_aliased_context():
    context1 = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    context2 = Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2)
    contexts_repository = ContextsRepository(context1, context2)

    contexts_repository.update_from_config(
        {CONTEXT3: {HELP: CONTEXT_HELP_STRING3, ALIASES: [CONTEXT4, CONTEXT5]}}
    )

    new_context = Context(
        name=CONTEXT3, help=CONTEXT_HELP_STRING3, aliases=[CONTEXT4, CONTEXT5]
    )

    assert len(contexts_repository) == 3
    assert contexts_repository[CONTEXT1] == context1
    assert contexts_repository[CONTEXT2] == context2
    assert contexts_repository[CONTEXT3] == new_context
    assert contexts_repository[CONTEXT4] == new_context
    assert contexts_repository[CONTEXT5] == new_context


def test_contexts_repository_update_adds_allowed_by_default_context():
    context1 = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    context2 = Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2)
    contexts_repository = ContextsRepository(context1, context2)

    contexts_repository.update_from_config(
        {CONTEXT3: {HELP: CONTEXT_HELP_STRING3, ALLOWED_BY_DEFAULT: True}}
    )

    assert len(contexts_repository) == 3
    assert contexts_repository[CONTEXT1] == context1
    assert contexts_repository[CONTEXT2] == context2
    assert contexts_repository[CONTEXT3] == Context(
        name=CONTEXT3, help=CONTEXT_HELP_STRING3, allowed_by_default=True
    )


def test_contexts_repository_update_adds_context_with_existing_parent():
    context1 = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    context2 = Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2)
    contexts_repository = ContextsRepository(context1, context2)

    contexts_repository.update_from_config(
        {CONTEXT3: {HELP: CONTEXT_HELP_STRING3, PARENT: CONTEXT1}}
    )

    assert len(contexts_repository) == 3
    assert contexts_repository[CONTEXT1] == context1
    assert contexts_repository[CONTEXT2] == context2
    assert contexts_repository[CONTEXT3] == Context(
        name=CONTEXT3, help=CONTEXT_HELP_STRING3, parent=context1
    )


def test_contexts_repository_update_adds_two_contexts():
    context1 = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    context2 = Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2)
    contexts_repository = ContextsRepository(context1, context2)

    contexts_repository.update_from_config(
        {
            CONTEXT3: {HELP: CONTEXT_HELP_STRING3},
            CONTEXT4: {
                HELP: CONTEXT_HELP_STRING4,
                ALLOWED_BY_DEFAULT: True,
            },
        }
    )

    assert len(contexts_repository) == 4
    assert contexts_repository[CONTEXT1] == context1
    assert contexts_repository[CONTEXT2] == context2
    assert contexts_repository[CONTEXT3] == Context(
        name=CONTEXT3, help=CONTEXT_HELP_STRING3
    )
    assert contexts_repository[CONTEXT4] == Context(
        name=CONTEXT4, help=CONTEXT_HELP_STRING4, allowed_by_default=True
    )


def test_contexts_repository_update_adds_context_with_new_parent():
    context1 = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    context2 = Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2)
    contexts_repository = ContextsRepository(context1, context2)

    contexts_repository.update_from_config(
        {
            CONTEXT3: {HELP: CONTEXT_HELP_STRING3, PARENT: CONTEXT4},
            CONTEXT4: {
                HELP: CONTEXT_HELP_STRING4,
                ALLOWED_BY_DEFAULT: True,
            },
        }
    )

    new_parent = Context(
        name=CONTEXT4, help=CONTEXT_HELP_STRING4, allowed_by_default=True
    )

    assert len(contexts_repository) == 4
    assert contexts_repository[CONTEXT1] == context1
    assert contexts_repository[CONTEXT2] == context2
    assert contexts_repository[CONTEXT3] == Context(
        name=CONTEXT3, help=CONTEXT_HELP_STRING3, parent=new_parent
    )
    assert contexts_repository[CONTEXT4] == new_parent


def test_contexts_repository_update_fail_redefining_same_context():
    context1 = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    context2 = Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2)
    contexts_repository = ContextsRepository(context1, context2)

    with pytest.raises(
        InconsistentConfiguration,
        match=f'^"{CONTEXT1}" is a already defined context and cannot defined twice$',
    ):
        contexts_repository.update_from_config(
            {CONTEXT1: {HELP: CONTEXT_HELP_STRING3, ALLOWED_BY_DEFAULT: True}}
        )

    assert len(contexts_repository) == 2
    assert contexts_repository[CONTEXT1] == context1
    assert contexts_repository[CONTEXT2] == context2


def test_contexts_repository_update_fail_aliasing_existing_context():
    context1 = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    context2 = Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2)
    contexts_repository = ContextsRepository(context1, context2)

    with pytest.raises(
        InconsistentConfiguration,
        match=(
            f'^"{CONTEXT1}" cannot be defined as an alias for "{CONTEXT3}" '
            "because a context is already defined with this name$"
        ),
    ):
        contexts_repository.update_from_config(
            {
                CONTEXT3: {
                    HELP: CONTEXT_HELP_STRING3,
                    ALLOWED_BY_DEFAULT: True,
                    ALIASES: [CONTEXT1],
                }
            }
        )

    assert len(contexts_repository) == 2
    assert contexts_repository[CONTEXT1] == context1
    assert contexts_repository[CONTEXT2] == context2
