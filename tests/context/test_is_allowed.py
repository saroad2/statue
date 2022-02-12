from statue.constants import ALLOWED_CONTEXTS, REQUIRED_CONTEXTS, STANDARD
from statue.context import Context
from tests.constants import (
    CONTEXT1,
    CONTEXT2,
    CONTEXT3,
    CONTEXT4,
    CONTEXT5,
    CONTEXT6,
    CONTEXT_HELP_STRING1,
    STANDARD_HELP,
)


def test_default_context_is_allowed():
    context = Context(name=STANDARD, help=STANDARD_HELP, is_default=True)
    setups = {}

    assert context.is_allowed(setups)


def test_required_context_is_allowed():
    context = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    setups = {REQUIRED_CONTEXTS: [CONTEXT1]}

    assert context.is_allowed(setups)


def test_required_context_alias_is_allowed():
    context = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1, aliases=[CONTEXT2])
    setups = {REQUIRED_CONTEXTS: [CONTEXT2]}

    assert context.is_allowed(setups)


def test_allowed_context_is_allowed():
    context = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    setups = {ALLOWED_CONTEXTS: [CONTEXT1]}

    assert context.is_allowed(setups)


def test_allowed_context_alias_is_allowed():
    context = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1, aliases=[CONTEXT2])
    setups = {ALLOWED_CONTEXTS: [CONTEXT2]}

    assert context.is_allowed(setups)


def test_context_allowed_with_context_setup():
    context = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    setups = {CONTEXT1: dict(args=["a", "b", "c"])}

    assert context.is_allowed(setups)


def test_context_allowed_with_context_alias_setup():
    context = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1, aliases=[CONTEXT2])
    setups = {CONTEXT2: dict(args=["a", "b", "c"])}

    assert context.is_allowed(setups)


def test_context_parent_is_allowed():
    parent = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    context = Context(name=CONTEXT2, help=CONTEXT_HELP_STRING1, parent=parent)
    setups = {ALLOWED_CONTEXTS: [CONTEXT1]}

    assert context.is_allowed(setups)


def test_context_parent_alias_is_allowed():
    parent = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1, aliases=[CONTEXT2])
    context = Context(name=CONTEXT3, help=CONTEXT_HELP_STRING1, parent=parent)
    setups = {ALLOWED_CONTEXTS: [CONTEXT2]}

    assert context.is_allowed(setups)


def test_context_is_not_allowed():
    parent = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1, aliases=[CONTEXT2])
    context = Context(name=CONTEXT3, help=CONTEXT_HELP_STRING1, parent=parent)
    setups = {
        ALLOWED_CONTEXTS: [CONTEXT4],
        REQUIRED_CONTEXTS: [CONTEXT5],
        CONTEXT6: dict(args=["a", "b", "c"]),
    }

    assert not context.is_allowed(setups)
