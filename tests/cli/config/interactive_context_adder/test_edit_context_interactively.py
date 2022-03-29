from statue.cli.config.interactive_adders.interactive_context_adder import (
    InteractiveContextAdder,
)
from statue.config.contexts_repository import ContextsRepository
from statue.context import Context
from tests.constants import (
    CONTEXT1,
    CONTEXT2,
    CONTEXT3,
    CONTEXT4,
    CONTEXT_HELP_STRING1,
    CONTEXT_HELP_STRING2,
    CONTEXT_HELP_STRING3,
)


def test_edit_context_interactively_change_help_string(cli_runner):
    contexts_repository = ContextsRepository(
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING2)
    )
    assert len(contexts_repository) == 1

    with cli_runner.isolation(input=f"{CONTEXT_HELP_STRING1}\n"):
        InteractiveContextAdder.edit_context(
            name=CONTEXT1, contexts_repository=contexts_repository
        )

    assert len(contexts_repository) == 1
    assert contexts_repository[CONTEXT1] == Context(
        name=CONTEXT1, help=CONTEXT_HELP_STRING1
    )


def test_edit_context_interactively_ask_again_for_help_string(cli_runner):
    contexts_repository = ContextsRepository(
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING2)
    )
    assert len(contexts_repository) == 1

    with cli_runner.isolation(input=f"\n\n{CONTEXT_HELP_STRING1}\n"):
        InteractiveContextAdder.edit_context(
            name=CONTEXT1, contexts_repository=contexts_repository
        )

    assert len(contexts_repository) == 1
    assert contexts_repository[CONTEXT1] == Context(
        name=CONTEXT1, help=CONTEXT_HELP_STRING1
    )


def test_edit_context_interactively_adds_aliases(cli_runner):
    contexts_repository = ContextsRepository(
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    )
    assert len(contexts_repository) == 1

    with cli_runner.isolation(
        input=(
            f"{CONTEXT_HELP_STRING1}\n"  # help string
            f"{CONTEXT2}, {CONTEXT3}\n"  # aliases
        )
    ):
        InteractiveContextAdder.edit_context(
            name=CONTEXT1, contexts_repository=contexts_repository
        )

    assert len(contexts_repository) == 1
    assert contexts_repository[CONTEXT1] == Context(
        name=CONTEXT1, help=CONTEXT_HELP_STRING1, aliases=[CONTEXT2, CONTEXT3]
    )


def test_edit_context_interactively_changes_aliases(cli_runner):
    contexts_repository = ContextsRepository(
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1, aliases=[CONTEXT2, CONTEXT4])
    )
    assert len(contexts_repository) == 1

    with cli_runner.isolation(
        input=(
            f"{CONTEXT_HELP_STRING1}\n"  # help string
            f"{CONTEXT2}, {CONTEXT3}\n"  # aliases
        )
    ):
        InteractiveContextAdder.edit_context(
            name=CONTEXT1, contexts_repository=contexts_repository
        )

    assert len(contexts_repository) == 1
    assert contexts_repository[CONTEXT1] == Context(
        name=CONTEXT1, help=CONTEXT_HELP_STRING1, aliases=[CONTEXT2, CONTEXT3]
    )


def test_edit_context_interactively_with_preexisting_alias_of_other_context(cli_runner):
    contexts_repository = ContextsRepository(
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
        Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2),
    )
    assert len(contexts_repository) == 2

    with cli_runner.isolation(
        input=(
            f"{CONTEXT_HELP_STRING1}\n"  # help string
            f"{CONTEXT2}, {CONTEXT3}\n"  # aliases fail
            f"{CONTEXT4}, {CONTEXT3}\n"  # retry aliases success
        )
    ):
        InteractiveContextAdder.edit_context(
            name=CONTEXT1, contexts_repository=contexts_repository
        )

    assert len(contexts_repository) == 2
    assert contexts_repository[CONTEXT1] == Context(
        name=CONTEXT1, help=CONTEXT_HELP_STRING1, aliases=[CONTEXT4, CONTEXT3]
    )
    assert contexts_repository[CONTEXT2] == Context(
        name=CONTEXT2, help=CONTEXT_HELP_STRING2
    )


def test_edit_context_interactively_with_self_alias(cli_runner):
    contexts_repository = ContextsRepository(
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
        Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2),
    )
    assert len(contexts_repository) == 2

    with cli_runner.isolation(
        input=(
            f"{CONTEXT_HELP_STRING1}\n"  # help string
            f"{CONTEXT1}, {CONTEXT3}\n"  # ignore self name
        )
    ):
        InteractiveContextAdder.edit_context(
            name=CONTEXT1, contexts_repository=contexts_repository
        )

    assert len(contexts_repository) == 2
    assert contexts_repository[CONTEXT1] == Context(
        name=CONTEXT1, help=CONTEXT_HELP_STRING1, aliases=[CONTEXT3]
    )
    assert contexts_repository[CONTEXT2] == Context(
        name=CONTEXT2, help=CONTEXT_HELP_STRING2
    )


def test_edit_context_interactively_with_parent(cli_runner):
    parent = Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2)
    contexts_repository = ContextsRepository(
        parent, Context(name=CONTEXT1, help=CONTEXT_HELP_STRING3)
    )
    assert len(contexts_repository) == 2

    with cli_runner.isolation(
        input=(
            f"{CONTEXT_HELP_STRING1}\n"  # help string
            "\n"  # no aliases
            f"{CONTEXT2}\n"  # parent
        )
    ):
        InteractiveContextAdder.edit_context(
            name=CONTEXT1, contexts_repository=contexts_repository
        )

    assert len(contexts_repository) == 2
    assert contexts_repository[CONTEXT1] == Context(
        name=CONTEXT1, help=CONTEXT_HELP_STRING1, parent=parent
    )
    assert contexts_repository[CONTEXT2] == parent


def test_edit_context_interactively_with_non_existing_parent(cli_runner):
    parent = Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2)
    contexts_repository = ContextsRepository(
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING3), parent
    )
    assert len(contexts_repository) == 2

    with cli_runner.isolation(
        input=(
            f"{CONTEXT_HELP_STRING1}\n"  # help string
            "\n"  # no aliases
            f"{CONTEXT3}\n"  # non existing parent
            f"{CONTEXT2}\n"  # retry existing parent
        )
    ):
        InteractiveContextAdder.edit_context(
            name=CONTEXT1, contexts_repository=contexts_repository
        )

    assert len(contexts_repository) == 2
    assert contexts_repository[CONTEXT1] == Context(
        name=CONTEXT1, help=CONTEXT_HELP_STRING1, parent=parent
    )
    assert contexts_repository[CONTEXT2] == parent


def test_edit_context_interactively_with_self_as_parent(cli_runner):
    parent = Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2)
    contexts_repository = ContextsRepository(
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING3), parent
    )
    assert len(contexts_repository) == 2

    with cli_runner.isolation(
        input=(
            f"{CONTEXT_HELP_STRING1}\n"  # help string
            "\n"  # no aliases
            f"{CONTEXT1}\n"  # can't be a parent of self
            f"{CONTEXT2}\n"  # retry existing parent
        )
    ):
        InteractiveContextAdder.edit_context(
            name=CONTEXT1, contexts_repository=contexts_repository
        )

    assert len(contexts_repository) == 2
    assert contexts_repository[CONTEXT1] == Context(
        name=CONTEXT1, help=CONTEXT_HELP_STRING1, parent=parent
    )
    assert contexts_repository[CONTEXT2] == parent


def test_edit_context_interactively_with_alias_as_parent(cli_runner):
    parent = Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2)
    contexts_repository = ContextsRepository(
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING3), parent
    )
    assert len(contexts_repository) == 2

    with cli_runner.isolation(
        input=(
            f"{CONTEXT_HELP_STRING1}\n"  # help string
            f"{CONTEXT3}, {CONTEXT4}\n"  # two aliases
            f"{CONTEXT3}\n"  # can't be a parent of self
            f"{CONTEXT2}\n"  # retry existing parent
        )
    ):
        InteractiveContextAdder.edit_context(
            name=CONTEXT1, contexts_repository=contexts_repository
        )

    assert len(contexts_repository) == 2
    assert contexts_repository[CONTEXT1] == Context(
        name=CONTEXT1,
        help=CONTEXT_HELP_STRING1,
        aliases=[CONTEXT3, CONTEXT4],
        parent=parent,
    )
    assert contexts_repository[CONTEXT2] == parent


def test_edit_context_interactively_allowed_by_default(cli_runner):
    contexts_repository = ContextsRepository(
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING2)
    )
    assert len(contexts_repository) == 1

    with cli_runner.isolation(
        input=(
            f"{CONTEXT_HELP_STRING1}\n"  # help string
            "\n"  # no aliases
            "\n"  # no parent
            "y\n"  # allowed by default
        )
    ):
        InteractiveContextAdder.edit_context(
            name=CONTEXT1, contexts_repository=contexts_repository
        )

    assert len(contexts_repository) == 1
    assert contexts_repository[CONTEXT1] == Context(
        name=CONTEXT1, help=CONTEXT_HELP_STRING1, allowed_by_default=True
    )


def test_edit_context_interactively_with_everything(cli_runner):
    parent = Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2)
    contexts_repository = ContextsRepository(
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING3), parent
    )
    assert len(contexts_repository) == 2

    with cli_runner.isolation(
        input=(
            f"{CONTEXT_HELP_STRING1}\n"  # help string
            f"{CONTEXT3}, {CONTEXT4}\n"  # two aliases
            f"{CONTEXT2}\n"  # retry existing parent
            "y\n"  # allowed by default
        )
    ):
        InteractiveContextAdder.edit_context(
            name=CONTEXT1, contexts_repository=contexts_repository
        )

    assert len(contexts_repository) == 2
    assert contexts_repository[CONTEXT1] == Context(
        name=CONTEXT1,
        help=CONTEXT_HELP_STRING1,
        aliases=[CONTEXT3, CONTEXT4],
        parent=parent,
        allowed_by_default=True,
    )
    assert contexts_repository[CONTEXT2] == parent
