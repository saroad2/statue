from statue.cli import statue_cli
from statue.configuration import Configuration
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
    CONTEXT_HELP_STRING4,
    CONTEXT_HELP_STRING5,
    NOT_EXISTING_CONTEXT,
)


def test_contexts_list_of_full_configuration(
    cli_runner, clear_configuration, mock_load_configuration
):
    Configuration.contexts_repository.add_contexts(
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
        Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2),
        Context(name=CONTEXT3, help=CONTEXT_HELP_STRING3),
        Context(name=CONTEXT4, help=CONTEXT_HELP_STRING4),
        Context(name=CONTEXT5, help=CONTEXT_HELP_STRING5),
    )
    result = cli_runner.invoke(statue_cli, ["context", "list"])
    assert result.exit_code == 0, "list contexts should exit with success."
    assert result.output == (
        f"{CONTEXT1} - {CONTEXT_HELP_STRING1}\n"
        f"{CONTEXT2} - {CONTEXT_HELP_STRING2}\n"
        f"{CONTEXT3} - {CONTEXT_HELP_STRING3}\n"
        f"{CONTEXT4} - {CONTEXT_HELP_STRING4}\n"
        f"{CONTEXT5} - {CONTEXT_HELP_STRING5}\n"
    ), "List output is different than expected."


def test_contexts_list_of_an_clear_configuration(
    cli_runner, clear_configuration, mock_load_configuration
):
    result = cli_runner.invoke(statue_cli, ["context", "list"])
    assert result.exit_code == 1, "list contexts should exit with failure."
    assert (
        result.output == "No contexts were found.\n"
    ), "List output is different than expected."


def test_contexts_show_of_context(cli_runner, clear_configuration):
    Configuration.contexts_repository.add_contexts(
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
        Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2),
        Context(name=CONTEXT3, help=CONTEXT_HELP_STRING3),
        Context(name=CONTEXT4, help=CONTEXT_HELP_STRING4),
        Context(name=CONTEXT5, help=CONTEXT_HELP_STRING5),
    )
    result = cli_runner.invoke(statue_cli, ["context", "show", CONTEXT2])
    assert result.exit_code == 0, "show context should exit with success."
    assert result.output == (
        f"Name - {CONTEXT2}\n" f"Description - {CONTEXT_HELP_STRING2}\n"
    ), "Show output is different than expected."


def test_contexts_show_of_context_with_one_alias(cli_runner, clear_configuration):
    Configuration.contexts_repository.add_contexts(
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1, aliases=[CONTEXT2])
    )
    result = cli_runner.invoke(statue_cli, ["context", "show", CONTEXT1])
    assert result.exit_code == 0, "show context should exit with success."
    assert result.output == (
        f"Name - {CONTEXT1}\n"
        f"Description - {CONTEXT_HELP_STRING1}\n"
        f"Aliases - {CONTEXT2}\n"
    ), "Show output is different than expected."


def test_contexts_show_of_context_with_by_alias(cli_runner, clear_configuration):
    Configuration.contexts_repository.add_contexts(
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1, aliases=[CONTEXT2])
    )
    result = cli_runner.invoke(statue_cli, ["context", "show", CONTEXT2])
    assert result.exit_code == 0, "show context should exit with success."
    assert result.output == (
        f"Name - {CONTEXT1}\n"
        f"Description - {CONTEXT_HELP_STRING1}\n"
        f"Aliases - {CONTEXT2}\n"
    ), "Show output is different than expected."


def test_contexts_show_of_context_with_two_aliases(cli_runner, clear_configuration):
    Configuration.contexts_repository.add_contexts(
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1, aliases=[CONTEXT2, CONTEXT3])
    )
    result = cli_runner.invoke(statue_cli, ["context", "show", CONTEXT1])
    assert result.exit_code == 0, "show context should exit with success."
    assert result.output == (
        f"Name - {CONTEXT1}\n"
        f"Description - {CONTEXT_HELP_STRING1}\n"
        f"Aliases - {CONTEXT2}, {CONTEXT3}\n"
    ), "Show output is different than expected."


def test_contexts_show_of_context_with_parent(cli_runner, clear_configuration):
    parent = Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2)
    context = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1, parent=parent)
    Configuration.contexts_repository.add_contexts(context, parent)
    result = cli_runner.invoke(statue_cli, ["context", "show", CONTEXT1])
    assert result.exit_code == 0, "show context should exit with success."
    assert result.output == (
        f"Name - {CONTEXT1}\n"
        f"Description - {CONTEXT_HELP_STRING1}\n"
        f"Parent - {CONTEXT2}\n"
    ), "Show output is different than expected."


def test_contexts_show_of_non_existing_context(cli_runner, clear_configuration):
    Configuration.contexts_repository.add_contexts(
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
        Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2),
        Context(name=CONTEXT3, help=CONTEXT_HELP_STRING3),
        Context(name=CONTEXT4, help=CONTEXT_HELP_STRING4),
        Context(name=CONTEXT5, help=CONTEXT_HELP_STRING5),
    )
    result = cli_runner.invoke(statue_cli, ["context", "show", NOT_EXISTING_CONTEXT])
    assert result.exit_code == 1, "show context should exit with failure."
    assert (
        result.output == f'Could not find the context "{NOT_EXISTING_CONTEXT}".\n'
    ), "Show output is different than expected."
