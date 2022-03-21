import pytest

from statue.cli.interactive_sources_adder import InteractiveSourcesAdder
from statue.command_builder import CommandBuilder
from statue.commands_filter import CommandsFilter
from statue.config.configuration import Configuration
from statue.context import Context
from tests.constants import (
    COMMAND1,
    COMMAND2,
    COMMAND3,
    COMMAND4,
    COMMAND_HELP_STRING1,
    COMMAND_HELP_STRING2,
    COMMAND_HELP_STRING3,
    CONTEXT1,
    CONTEXT2,
    CONTEXT3,
    CONTEXT4,
    CONTEXT_HELP_STRING1,
    CONTEXT_HELP_STRING2,
    CONTEXT_HELP_STRING3,
    SOURCE1,
    SOURCE2,
    SOURCE3,
)

yes_parametrization = pytest.mark.parametrize(
    argnames="yes_word", argvalues=["", "y", "yes", "YES"]
)
no_parametrization = pytest.mark.parametrize(
    argnames="no_word", argvalues=["n", "no", "NO"]
)
expend_parametrization = pytest.mark.parametrize(
    argnames="expend_word", argvalues=["e", "expend", "EXPEND"]
)


def dummy_configuration():
    configuration = Configuration()
    configuration.contexts_repository.add_contexts(
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
        Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2),
        Context(name=CONTEXT3, help=CONTEXT_HELP_STRING3),
    )
    configuration.commands_repository.add_command_builders(
        CommandBuilder(name=COMMAND1, help=COMMAND_HELP_STRING1),
        CommandBuilder(name=COMMAND2, help=COMMAND_HELP_STRING2),
        CommandBuilder(name=COMMAND3, help=COMMAND_HELP_STRING3),
    )
    return configuration


@yes_parametrization
def test_interactive_sources_adder_one_source_simple_addition(
    yes_word, cli_runner, tmp_path
):
    source_path = tmp_path / SOURCE1
    source_path.touch()
    configuration = dummy_configuration()
    with cli_runner.isolation(input=f"{yes_word}\n"):
        InteractiveSourcesAdder.update_sources_repository(
            configuration=configuration, sources=[source_path]
        )

    assert configuration.sources_repository.sources_list == [source_path]
    assert configuration.sources_repository[source_path] == CommandsFilter()


@no_parametrization
def test_interactive_sources_adder_no_addition(no_word, cli_runner, tmp_path):
    source_path = tmp_path / SOURCE1
    source_path.touch()
    configuration = Configuration()
    with cli_runner.isolation(input=f"{no_word}\n"):
        InteractiveSourcesAdder.update_sources_repository(
            configuration=configuration, sources=[source_path]
        )

    assert len(configuration.sources_repository) == 0


def test_interactive_sources_adder_one_source_with_context(cli_runner, tmp_path):
    source_path = tmp_path / SOURCE1
    source_path.touch()
    configuration = dummy_configuration()
    with cli_runner.isolation(input=f"y\n{CONTEXT1}, {CONTEXT3}\n"):
        InteractiveSourcesAdder.update_sources_repository(
            configuration=configuration, sources=[source_path]
        )

    assert configuration.sources_repository.sources_list == [source_path]
    assert configuration.sources_repository[source_path] == CommandsFilter(
        contexts=[
            Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
            Context(name=CONTEXT3, help=CONTEXT_HELP_STRING3),
        ]
    )


def test_interactive_sources_adder_one_source_with_allowed_commands(
    cli_runner, tmp_path
):
    source_path = tmp_path / SOURCE1
    source_path.touch()
    configuration = dummy_configuration()
    with cli_runner.isolation(input=f"y\n\n{COMMAND1}, {COMMAND3}\n"):
        InteractiveSourcesAdder.update_sources_repository(
            configuration=configuration, sources=[source_path]
        )

    assert configuration.sources_repository.sources_list == [source_path]
    assert configuration.sources_repository[source_path] == CommandsFilter(
        allowed_commands=[COMMAND1, COMMAND3]
    )


def test_interactive_sources_adder_one_source_with_denied_commands(
    cli_runner, tmp_path
):
    source_path = tmp_path / SOURCE1
    source_path.touch()
    configuration = dummy_configuration()
    with cli_runner.isolation(input=f"y\n\n\n{COMMAND1}, {COMMAND3}\n"):
        InteractiveSourcesAdder.update_sources_repository(
            configuration=configuration, sources=[source_path]
        )

    assert configuration.sources_repository.sources_list == [source_path]
    assert configuration.sources_repository[source_path] == CommandsFilter(
        denied_commands=[COMMAND1, COMMAND3]
    )


def test_interactive_sources_adder_one_source_with_retry_context(cli_runner, tmp_path):
    source_path = tmp_path / SOURCE1
    source_path.touch()
    configuration = dummy_configuration()
    with cli_runner.isolation(
        input=(
            "y\n"
            f"{CONTEXT4}\n"  # Try non-existing context
            f"{CONTEXT1}, {CONTEXT3}\n"  # Try existing contexts
        )
    ):
        InteractiveSourcesAdder.update_sources_repository(
            configuration=configuration, sources=[source_path]
        )

    assert configuration.sources_repository.sources_list == [source_path]
    assert configuration.sources_repository[source_path] == CommandsFilter(
        contexts=[
            Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
            Context(name=CONTEXT3, help=CONTEXT_HELP_STRING3),
        ]
    )


def test_interactive_sources_adder_one_source_with_retry_allowed_commands(
    cli_runner, tmp_path
):
    source_path = tmp_path / SOURCE1
    source_path.touch()
    configuration = dummy_configuration()
    with cli_runner.isolation(
        input=(
            "y\n"
            "\n"  # no contexts
            f"{COMMAND4}\n"  # Try non-existing command
            f"{COMMAND1}, {COMMAND3}\n"  # Try existing commands
        )
    ):
        InteractiveSourcesAdder.update_sources_repository(
            configuration=configuration, sources=[source_path]
        )

    assert configuration.sources_repository.sources_list == [source_path]
    assert configuration.sources_repository[source_path] == CommandsFilter(
        allowed_commands=[COMMAND1, COMMAND3]
    )


def test_interactive_sources_adder_one_source_with_retry_denied_commands(
    cli_runner, tmp_path
):
    source_path = tmp_path / SOURCE1
    source_path.touch()
    configuration = dummy_configuration()
    with cli_runner.isolation(
        input=(
            "y\n"
            "\n"  # no contexts
            "\n"  # no allowed commands
            f"{COMMAND4}\n"  # Try non-existing command
            f"{COMMAND1}, {COMMAND3}\n"  # Try existing commands
        )
    ):
        InteractiveSourcesAdder.update_sources_repository(
            configuration=configuration, sources=[source_path]
        )

    assert configuration.sources_repository.sources_list == [source_path]
    assert configuration.sources_repository[source_path] == CommandsFilter(
        denied_commands=[COMMAND1, COMMAND3]
    )


def test_interactive_sources_adder_fail_adding_both_allowed_and_denied(
    cli_runner, tmp_path
):
    source_path = tmp_path / SOURCE1
    source_path.touch()
    configuration = dummy_configuration()
    with cli_runner.isolation(
        input=(
            "y\n"
            "\n"  # no contexts
            f"{COMMAND2}\n"  # allowed commands
            f"{COMMAND1}, {COMMAND3}\n"  # denied commands, fail here
            "\n"  # no contexts
            f"{COMMAND2}\n"  # allowed commands
            f"\n"  # no denied commands
        )
    ):
        InteractiveSourcesAdder.update_sources_repository(
            configuration=configuration, sources=[source_path]
        )

    assert configuration.sources_repository.sources_list == [source_path]
    assert configuration.sources_repository[source_path] == CommandsFilter(
        allowed_commands=[COMMAND2]
    )


@expend_parametrization
def test_interactive_sources_adder_expend_directory(expend_word, cli_runner, tmp_path):
    dir_path = tmp_path / "dir"
    dir_path.mkdir()
    source_path1, source_path2, source_path3 = (
        dir_path / f"{SOURCE1}.py",
        dir_path / f"{SOURCE2}.py",
        dir_path / f"{SOURCE3}.py",
    )
    source_path1.touch()
    source_path2.touch()
    source_path3.touch()
    configuration = dummy_configuration()
    with cli_runner.isolation(input=f"{expend_word}\n"):
        InteractiveSourcesAdder.update_sources_repository(
            configuration=configuration, sources=[dir_path]
        )

    assert configuration.sources_repository.sources_list == [
        source_path1,
        source_path2,
        source_path3,
    ]
    assert configuration.sources_repository[source_path1] == CommandsFilter()
    assert configuration.sources_repository[source_path2] == CommandsFilter()
    assert configuration.sources_repository[source_path3] == CommandsFilter()


def test_interactive_sources_adder_add_two_sources(cli_runner, tmp_path):
    source_path1, source_path2 = tmp_path / SOURCE1, tmp_path / SOURCE2
    source_path1.touch()
    source_path2.touch()
    configuration = dummy_configuration()
    with cli_runner.isolation(input="y\n"):
        InteractiveSourcesAdder.update_sources_repository(
            configuration=configuration, sources=[source_path1, source_path2]
        )

    assert configuration.sources_repository.sources_list == [source_path1, source_path2]
    assert configuration.sources_repository[source_path1] == CommandsFilter()
    assert configuration.sources_repository[source_path2] == CommandsFilter()


def test_interactive_sources_adder_one_source_with_no_contexts(cli_runner, tmp_path):
    source_path = tmp_path / SOURCE1
    source_path.touch()
    configuration = dummy_configuration()
    configuration.contexts_repository.reset()
    with cli_runner.isolation(
        input=(
            "y\n"
            # Do not ask for contexts
            f"{COMMAND1}, {COMMAND3}\n"
        )
    ):
        InteractiveSourcesAdder.update_sources_repository(
            configuration=configuration, sources=[source_path]
        )

    assert configuration.sources_repository.sources_list == [source_path]
    assert configuration.sources_repository[source_path] == CommandsFilter(
        allowed_commands=[COMMAND1, COMMAND3]
    )


def test_interactive_sources_adder_one_source_with_no_commands(cli_runner, tmp_path):
    source_path1, source_path2 = tmp_path / SOURCE1, tmp_path / SOURCE2
    source_path1.touch()
    source_path2.touch()
    configuration = dummy_configuration()
    configuration.commands_repository.reset()
    with cli_runner.isolation(
        input=(
            "y\n"
            f"{CONTEXT1}, {CONTEXT3}\n"
            # Do not ask for commands
            "y\n"
            f"{CONTEXT2}, {CONTEXT3}\n"
        )
    ):
        InteractiveSourcesAdder.update_sources_repository(
            configuration=configuration, sources=[source_path1, source_path2]
        )

    assert configuration.sources_repository.sources_list == [source_path1, source_path2]
    assert configuration.sources_repository[source_path1] == CommandsFilter(
        contexts=[
            Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
            Context(name=CONTEXT3, help=CONTEXT_HELP_STRING3),
        ]
    )
    assert configuration.sources_repository[source_path2] == CommandsFilter(
        contexts=[
            Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2),
            Context(name=CONTEXT3, help=CONTEXT_HELP_STRING3),
        ]
    )
