import pytest

from statue.config.contexts_repository import ContextsRepository
from statue.constants import ALIASES, ALLOWED_BY_DEFAULT, HELP, PARENT
from statue.context import Context
from statue.exceptions import InconsistentConfiguration, InvalidConfiguration
from tests.constants import (
    CONTEXT1,
    CONTEXT2,
    CONTEXT3,
    CONTEXT_HELP_STRING1,
    CONTEXT_HELP_STRING2,
    CONTEXT_HELP_STRING3,
)


def test_contexts_repository_from_empty_dict():
    contexts_repository = ContextsRepository.from_dict({})

    assert len(contexts_repository) == 0


def test_contexts_repository_from_dict_adds_new_simple_context():
    contexts_repository = ContextsRepository.from_dict(
        {CONTEXT1: {HELP: CONTEXT_HELP_STRING1}}
    )

    assert len(contexts_repository) == 1

    assert contexts_repository[CONTEXT1] == Context(
        name=CONTEXT1, help=CONTEXT_HELP_STRING1
    )


def test_contexts_repository_from_dict_adds_aliased_context():
    contexts_repository = ContextsRepository.from_dict(
        {CONTEXT1: {HELP: CONTEXT_HELP_STRING1, ALIASES: [CONTEXT2, CONTEXT3]}}
    )

    new_context = Context(
        name=CONTEXT1, help=CONTEXT_HELP_STRING1, aliases=[CONTEXT2, CONTEXT3]
    )

    assert len(contexts_repository) == 1

    assert contexts_repository[CONTEXT1] == new_context
    assert contexts_repository[CONTEXT2] == new_context
    assert contexts_repository[CONTEXT3] == new_context


def test_contexts_repository_from_dict_adds_allowed_by_default_context():
    contexts_repository = ContextsRepository.from_dict(
        {CONTEXT1: {HELP: CONTEXT_HELP_STRING1, ALLOWED_BY_DEFAULT: True}}
    )

    assert len(contexts_repository) == 1

    assert contexts_repository[CONTEXT1] == Context(
        name=CONTEXT1, help=CONTEXT_HELP_STRING1, allowed_by_default=True
    )


def test_contexts_repository_from_dict_adds_two_contexts():
    contexts_repository = ContextsRepository.from_dict(
        {
            CONTEXT1: {HELP: CONTEXT_HELP_STRING1},
            CONTEXT2: {
                HELP: CONTEXT_HELP_STRING2,
                ALLOWED_BY_DEFAULT: True,
            },
        }
    )

    assert len(contexts_repository) == 2

    assert contexts_repository[CONTEXT1] == Context(
        name=CONTEXT1, help=CONTEXT_HELP_STRING1
    )
    assert contexts_repository[CONTEXT2] == Context(
        name=CONTEXT2, help=CONTEXT_HELP_STRING2, allowed_by_default=True
    )


def test_contexts_repository_from_dict_adds_context_with_new_parent():

    contexts_repository = ContextsRepository.from_dict(
        {
            CONTEXT1: {HELP: CONTEXT_HELP_STRING1, PARENT: CONTEXT2},
            CONTEXT2: {
                HELP: CONTEXT_HELP_STRING2,
                ALLOWED_BY_DEFAULT: True,
            },
        }
    )

    new_parent = Context(
        name=CONTEXT2, help=CONTEXT_HELP_STRING2, allowed_by_default=True
    )

    assert len(contexts_repository) == 2

    assert contexts_repository[CONTEXT1] == Context(
        name=CONTEXT1, help=CONTEXT_HELP_STRING1, parent=new_parent
    )
    assert contexts_repository[CONTEXT2] == new_parent


def test_contexts_repository_from_dict_fail_redefining_same_context():
    with pytest.raises(InconsistentConfiguration):
        ContextsRepository.from_dict(
            {
                CONTEXT1: {
                    HELP: CONTEXT_HELP_STRING1,
                    ALLOWED_BY_DEFAULT: True,
                    ALIASES: [CONTEXT2],
                },
                CONTEXT2: {HELP: CONTEXT_HELP_STRING2},
            }
        )


def test_contexts_repository_from_dict_fail_on_unknown_parent():
    with pytest.raises(
        InconsistentConfiguration,
        match=(
            "^The following contexts cannot be built because they are missing or"
            f" they cause circular parenting: {CONTEXT1}$"
        ),
    ):
        ContextsRepository.from_dict(
            {
                CONTEXT1: {
                    HELP: CONTEXT_HELP_STRING1,
                    PARENT: CONTEXT2,
                },
            }
        )


def test_contexts_repository_from_dict_fail_on_circular_parenting_with_two_contexts():
    with pytest.raises(
        InconsistentConfiguration,
        match=(
            "^The following contexts cannot be built because they are missing or"
            " they cause circular parenting:"
        ),
    ):
        ContextsRepository.from_dict(
            {
                CONTEXT1: {
                    HELP: CONTEXT_HELP_STRING1,
                    PARENT: CONTEXT2,
                },
                CONTEXT2: {
                    HELP: CONTEXT_HELP_STRING2,
                    PARENT: CONTEXT1,
                },
            }
        )


def test_contexts_repository_from_dict_fail_on_circular_parenting_with_three_contexts():
    with pytest.raises(
        InconsistentConfiguration,
        match=(
            "^The following contexts cannot be built because they are missing or"
            " they cause circular parenting:"
        ),
    ):
        ContextsRepository.from_dict(
            {
                CONTEXT1: {
                    HELP: CONTEXT_HELP_STRING1,
                    PARENT: CONTEXT2,
                },
                CONTEXT2: {
                    HELP: CONTEXT_HELP_STRING2,
                    PARENT: CONTEXT3,
                },
                CONTEXT3: {
                    HELP: CONTEXT_HELP_STRING3,
                    PARENT: CONTEXT1,
                },
            }
        )


def test_contexts_repository_from_dict_fail_on_context_without_help():
    with pytest.raises(
        InvalidConfiguration, match=f"^Context {CONTEXT1} doesn't have help string$"
    ):
        ContextsRepository.from_dict({CONTEXT1: {}})
