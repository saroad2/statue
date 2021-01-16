from pytest_cases import THIS_MODULE, parametrize_with_cases

from statue.context import Context
from tests.constants import (
    CONTEXT1,
    CONTEXT2,
    CONTEXT3,
    CONTEXT4,
    CONTEXT5,
    CONTEXT_HELP_STRING1,
    CONTEXT_HELP_STRING2,
    CONTEXT_HELP_STRING3,
)

ITEM = dict(a=2, b=3)
ITEM2 = dict(c=8, d=-1)


def case_simple_context():
    context = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    setup = {CONTEXT1: ITEM}
    returned = ITEM
    return context, setup, returned


def case_context_with_alias():
    context = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1, aliases=[CONTEXT2])
    setup = {CONTEXT2: ITEM}
    returned = ITEM
    return context, setup, returned


def case_context_with_two_aliases():
    context = Context(
        name=CONTEXT1, help=CONTEXT_HELP_STRING1, aliases=[CONTEXT2, CONTEXT3]
    )
    setup = {CONTEXT3: ITEM}
    returned = ITEM
    return context, setup, returned


def case_context_choose_self_over_alias():
    context = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1, aliases=[CONTEXT2])
    setup = {CONTEXT1: ITEM, CONTEXT2: ITEM2}
    returned = ITEM
    return context, setup, returned


def case_context_with_parent():
    parent = Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2)
    context = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1, parent=parent)
    setup = {CONTEXT2: ITEM}
    returned = ITEM
    return context, setup, returned


def case_context_choose_self_over_parent():
    parent = Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2)
    context = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1, parent=parent)
    setup = {CONTEXT1: ITEM, CONTEXT2: ITEM2}
    returned = ITEM
    return context, setup, returned


def case_context_with_grandparent():
    grandparent = Context(name=CONTEXT3, help=CONTEXT_HELP_STRING3)
    parent = Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2, parent=grandparent)
    context = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1, parent=parent)
    setup = {CONTEXT3: ITEM}
    returned = ITEM
    return context, setup, returned


def case_context_choose_self_over_grandparent():
    grandparent = Context(name=CONTEXT3, help=CONTEXT_HELP_STRING3)
    parent = Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2, parent=grandparent)
    context = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1, parent=parent)
    setup = {CONTEXT1: ITEM, CONTEXT3: ITEM2}
    returned = ITEM
    return context, setup, returned


def case_default_context_in_setup():
    context = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1, is_default=True)
    setup = {CONTEXT1: ITEM}
    returned = ITEM
    return context, setup, returned


def case_default_context_not_in_setup():
    context = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1, is_default=True)
    setup = {CONTEXT2: ITEM}
    returned = setup
    return context, setup, returned


def case_default_context_is_parent():
    parent = Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2, is_default=True)
    context = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1, parent=parent)
    setup = {CONTEXT3: ITEM}
    returned = setup
    return context, setup, returned


def case_context_not_found():
    context = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    setup = {CONTEXT2: ITEM, CONTEXT3: ITEM2}
    returned = None
    return context, setup, returned


def case_context_and_parent_not_found():
    parent = Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2)
    context = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1, parent=parent)
    setup = {CONTEXT3: ITEM, CONTEXT4: ITEM2}
    returned = None
    return context, setup, returned


def case_and_grandparent_not_found():
    grandparent = Context(name=CONTEXT3, help=CONTEXT_HELP_STRING3)
    parent = Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2, parent=grandparent)
    context = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1, parent=parent)
    setup = {CONTEXT4: ITEM, CONTEXT5: ITEM2}
    returned = None
    return context, setup, returned


@parametrize_with_cases(argnames=["context", "setup", "returned"], cases=THIS_MODULE)
def test_search_in_context(context, setup, returned):
    assert returned == context.search_context(
        setup
    ), f"{returned} wasn't found in setup {setup} using context {context}"
