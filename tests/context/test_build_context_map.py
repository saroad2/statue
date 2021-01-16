import pytest
from pytest_cases import THIS_MODULE, parametrize_with_cases

from statue.constants import ALIASES, HELP, IS_DEFAULT, PARENT
from statue.context import Context
from statue.exceptions import UnknownContext
from tests.constants import (
    CONTEXT1,
    CONTEXT2,
    CONTEXT3,
    CONTEXT_HELP_STRING1,
    CONTEXT_HELP_STRING2,
)
from tests.util import build_contexts_map


def case_simple_context():
    context_config = {CONTEXT1: {HELP: CONTEXT_HELP_STRING1}}
    context1 = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    return context_config, build_contexts_map(context1)


def case_two_simple_contexts():
    context_config = {
        CONTEXT1: {HELP: CONTEXT_HELP_STRING1},
        CONTEXT2: {HELP: CONTEXT_HELP_STRING2},
    }
    context1 = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    context2 = Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2)
    return context_config, build_contexts_map(context1, context2)


def case_one_context_one_alias():
    context_config = {CONTEXT1: {HELP: CONTEXT_HELP_STRING1, ALIASES: [CONTEXT2]}}
    context1 = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1, aliases=[CONTEXT2])
    return context_config, build_contexts_map(context1)


def case_one_context_two_aliases():
    context_config = {
        CONTEXT1: {HELP: CONTEXT_HELP_STRING1, ALIASES: [CONTEXT2, CONTEXT3]}
    }
    context1 = Context(
        name=CONTEXT1, help=CONTEXT_HELP_STRING1, aliases=[CONTEXT2, CONTEXT3]
    )
    return context_config, build_contexts_map(context1)


def case_context_with_parent():
    context_config = {
        CONTEXT1: {HELP: CONTEXT_HELP_STRING1, PARENT: CONTEXT2},
        CONTEXT2: {HELP: CONTEXT_HELP_STRING2},
    }
    context2 = Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2)
    context1 = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1, parent=context2)
    return context_config, build_contexts_map(context1, context2)


def case_context_with_parent_with_alias():
    context_config = {
        CONTEXT1: {HELP: CONTEXT_HELP_STRING1, PARENT: CONTEXT2},
        CONTEXT2: {HELP: CONTEXT_HELP_STRING2, ALIASES: [CONTEXT3]},
    }
    context2 = Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2, aliases=[CONTEXT3])
    context1 = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1, parent=context2)
    return context_config, build_contexts_map(context1, context2)


def case_default_context():
    context_config = {CONTEXT1: {HELP: CONTEXT_HELP_STRING1, IS_DEFAULT: True}}
    context1 = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1, is_default=True)
    return context_config, build_contexts_map(context1)


def case_context_inheritance_from_default():
    context_config = {
        CONTEXT1: {HELP: CONTEXT_HELP_STRING1, IS_DEFAULT: True},
        CONTEXT2: {HELP: CONTEXT_HELP_STRING2, PARENT: CONTEXT1},
    }
    context1 = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1, is_default=True)
    context2 = Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2, parent=context1)
    return context_config, build_contexts_map(context1, context2)


@parametrize_with_cases(argnames=["context_config", "contexts_map"], cases=THIS_MODULE)
def test_build_contexts_map(context_config, contexts_map):
    assert (
        Context.build_contexts_map(context_config) == contexts_map
    ), "Contexts map is different than expected"


def test_config_with_unknown_parent_context():
    contexts_config = {CONTEXT1: {HELP: CONTEXT_HELP_STRING1, PARENT: CONTEXT2}}
    with pytest.raises(
        UnknownContext, match=f'^Could not find context named "{CONTEXT2}".$'
    ):
        Context.build_contexts_map(contexts_config)
