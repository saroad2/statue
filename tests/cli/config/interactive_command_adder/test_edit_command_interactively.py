from statue.cli.config.interactive_adders.interactive_command_adder import (
    InteractiveCommandAdder,
)
from statue.command_builder import CommandBuilder
from statue.context import Context
from statue.context_specification import ContextSpecification
from tests.constants import (
    ARG1,
    ARG2,
    ARG3,
    ARG4,
    COMMAND1,
    COMMAND_HELP_STRING1,
    CONTEXT1,
    CONTEXT2,
    CONTEXT3,
    CONTEXT_HELP_STRING1,
    CONTEXT_HELP_STRING2,
    CONTEXT_HELP_STRING3,
)
from tests.util import dummy_version


def test_interactive_edit_command_with_simple_command(cli_runner, empty_configuration):

    empty_configuration.commands_repository.add_command_builders(
        CommandBuilder(name=COMMAND1, help=COMMAND_HELP_STRING1)
    )
    assert len(empty_configuration.commands_repository) == 1

    with cli_runner.isolation(input=f"{COMMAND_HELP_STRING1}\n"):
        InteractiveCommandAdder.edit_command(COMMAND1, empty_configuration)

    assert len(empty_configuration.commands_repository) == 1
    assert empty_configuration.commands_repository[COMMAND1] == CommandBuilder(
        name=COMMAND1, help=COMMAND_HELP_STRING1
    )


def test_interactive_edit_command_re_ask_for_help_string(
    cli_runner, empty_configuration
):

    empty_configuration.commands_repository.add_command_builders(
        CommandBuilder(name=COMMAND1, help=COMMAND_HELP_STRING1)
    )
    assert len(empty_configuration.commands_repository) == 1

    with cli_runner.isolation(input=f"\n{COMMAND_HELP_STRING1}\n"):
        InteractiveCommandAdder.edit_command(COMMAND1, empty_configuration)

    assert len(empty_configuration.commands_repository) == 1
    assert empty_configuration.commands_repository[COMMAND1] == CommandBuilder(
        name=COMMAND1, help=COMMAND_HELP_STRING1
    )


def test_interactive_edit_command_with_default_args(cli_runner, empty_configuration):

    empty_configuration.commands_repository.add_command_builders(
        CommandBuilder(name=COMMAND1, help=COMMAND_HELP_STRING1)
    )
    assert len(empty_configuration.commands_repository) == 1

    with cli_runner.isolation(
        input=(
            f"{COMMAND_HELP_STRING1}\n"  # help string
            f"{ARG1} {ARG2}\n"  # default args
        )
    ):
        InteractiveCommandAdder.edit_command(COMMAND1, empty_configuration)

    assert len(empty_configuration.commands_repository) == 1
    assert empty_configuration.commands_repository[COMMAND1] == CommandBuilder(
        name=COMMAND1, help=COMMAND_HELP_STRING1, default_args=[ARG1, ARG2]
    )


def test_interactive_edit_command_with_version(cli_runner, empty_configuration):
    version = dummy_version()
    empty_configuration.commands_repository.add_command_builders(
        CommandBuilder(name=COMMAND1, help=COMMAND_HELP_STRING1)
    )
    assert len(empty_configuration.commands_repository) == 1

    with cli_runner.isolation(
        input=(
            f"{COMMAND_HELP_STRING1}\n"  # help string
            "\n"  # no default args
            f"{version}\n"  # version
        )
    ):
        InteractiveCommandAdder.edit_command(COMMAND1, empty_configuration)

    assert len(empty_configuration.commands_repository) == 1
    assert empty_configuration.commands_repository[COMMAND1] == CommandBuilder(
        name=COMMAND1, help=COMMAND_HELP_STRING1, version=version
    )


def test_interactive_edit_command_with_required_contexts(
    cli_runner, empty_configuration
):
    context1, context2 = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1), Context(
        name=CONTEXT2, help=CONTEXT_HELP_STRING2
    )
    empty_configuration.contexts_repository.add_contexts(context1, context2)
    empty_configuration.commands_repository.add_command_builders(
        CommandBuilder(name=COMMAND1, help=COMMAND_HELP_STRING1)
    )
    assert len(empty_configuration.commands_repository) == 1

    with cli_runner.isolation(
        input=(
            f"{COMMAND_HELP_STRING1}\n"  # help string
            "\n"  # no default args
            "\n"  # no version
            f"{CONTEXT1}, {CONTEXT2}"  # required contexts
        )
    ):
        InteractiveCommandAdder.edit_command(COMMAND1, empty_configuration)

    assert len(empty_configuration.commands_repository) == 1
    assert empty_configuration.commands_repository[COMMAND1] == CommandBuilder(
        name=COMMAND1, help=COMMAND_HELP_STRING1, required_contexts=[context1, context2]
    )


def test_interactive_edit_command_re_ask_for_required_contexts_due_to_unknown_context(
    cli_runner, empty_configuration
):
    context1, context2 = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1), Context(
        name=CONTEXT2, help=CONTEXT_HELP_STRING2
    )
    empty_configuration.contexts_repository.add_contexts(context1, context2)
    empty_configuration.commands_repository.add_command_builders(
        CommandBuilder(name=COMMAND1, help=COMMAND_HELP_STRING1)
    )
    assert len(empty_configuration.commands_repository) == 1

    with cli_runner.isolation(
        input=(
            f"{COMMAND_HELP_STRING1}\n"  # help string
            "\n"  # no default args
            "\n"  # no version
            f"{CONTEXT3}, {CONTEXT2}\n"  # required contexts, context3 is unknown
            f"{CONTEXT1}, {CONTEXT2}\n"  # required contexts
        )
    ):
        InteractiveCommandAdder.edit_command(COMMAND1, empty_configuration)

    assert len(empty_configuration.commands_repository) == 1
    assert empty_configuration.commands_repository[COMMAND1] == CommandBuilder(
        name=COMMAND1, help=COMMAND_HELP_STRING1, required_contexts=[context1, context2]
    )


def test_interactive_edit_command_with_allowed_contexts(
    cli_runner, empty_configuration
):
    context1, context2 = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1), Context(
        name=CONTEXT2, help=CONTEXT_HELP_STRING2
    )
    empty_configuration.contexts_repository.add_contexts(context1, context2)
    empty_configuration.commands_repository.add_command_builders(
        CommandBuilder(name=COMMAND1, help=COMMAND_HELP_STRING1)
    )
    assert len(empty_configuration.commands_repository) == 1

    with cli_runner.isolation(
        input=(
            f"{COMMAND_HELP_STRING1}\n"  # help string
            "\n"  # no default args
            "\n"  # no version
            "\n"  # no required contexts
            f"{CONTEXT1}, {CONTEXT2}"  # allowed contexts
        )
    ):
        InteractiveCommandAdder.edit_command(COMMAND1, empty_configuration)

    assert len(empty_configuration.commands_repository) == 1
    assert empty_configuration.commands_repository[COMMAND1] == CommandBuilder(
        name=COMMAND1, help=COMMAND_HELP_STRING1, allowed_contexts=[context1, context2]
    )


def test_interactive_edit_command_re_ask_for_allowed_contexts_due_to_unknown_context(
    cli_runner, empty_configuration
):
    context1, context2 = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1), Context(
        name=CONTEXT2, help=CONTEXT_HELP_STRING2
    )
    empty_configuration.contexts_repository.add_contexts(context1, context2)
    empty_configuration.commands_repository.add_command_builders(
        CommandBuilder(name=COMMAND1, help=COMMAND_HELP_STRING1)
    )
    assert len(empty_configuration.commands_repository) == 1

    with cli_runner.isolation(
        input=(
            f"{COMMAND_HELP_STRING1}\n"  # help string
            "\n"  # no default args
            "\n"  # no version
            "\n"  # no required contexts
            f"{CONTEXT3}, {CONTEXT2}\n"  # allowed contexts, context3 is unknown
            f"{CONTEXT1}, {CONTEXT2}\n"  # allowed contexts
        )
    ):
        InteractiveCommandAdder.edit_command(COMMAND1, empty_configuration)

    assert len(empty_configuration.commands_repository) == 1
    assert empty_configuration.commands_repository[COMMAND1] == CommandBuilder(
        name=COMMAND1, help=COMMAND_HELP_STRING1, allowed_contexts=[context1, context2]
    )


def test_interactive_edit_command_re_ask_for_allowed_contexts_due_to_taken_context(
    cli_runner, empty_configuration
):
    context1, context2, context3 = (
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
        Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2),
        Context(name=CONTEXT3, help=CONTEXT_HELP_STRING3),
    )
    empty_configuration.contexts_repository.add_contexts(context1, context2, context3)
    empty_configuration.commands_repository.add_command_builders(
        CommandBuilder(name=COMMAND1, help=COMMAND_HELP_STRING1)
    )
    assert len(empty_configuration.commands_repository) == 1

    with cli_runner.isolation(
        input=(
            f"{COMMAND_HELP_STRING1}\n"  # help string
            "\n"  # no default args
            "\n"  # no version
            f"{CONTEXT3}\n"  # required context
            f"{CONTEXT3}, {CONTEXT2}\n"  # allowed contexts, context3 is preoccupied
            f"{CONTEXT1}, {CONTEXT2}\n"  # allowed contexts
        )
    ):
        InteractiveCommandAdder.edit_command(COMMAND1, empty_configuration)

    assert len(empty_configuration.commands_repository) == 1
    assert empty_configuration.commands_repository[COMMAND1] == CommandBuilder(
        name=COMMAND1,
        help=COMMAND_HELP_STRING1,
        required_contexts=[context3],
        allowed_contexts=[context1, context2],
    )


def test_interactive_edit_command_with_args_override_context(
    cli_runner, empty_configuration
):
    context1 = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    empty_configuration.contexts_repository.add_contexts(context1)
    empty_configuration.commands_repository.add_command_builders(
        CommandBuilder(name=COMMAND1, help=COMMAND_HELP_STRING1)
    )
    assert len(empty_configuration.commands_repository) == 1

    with cli_runner.isolation(
        input=(
            f"{COMMAND_HELP_STRING1}\n"  # help string
            "\n"  # no default args
            "\n"  # no version
            "\n"  # no required contexts
            "\n"  # no allowed contexts
            f"{CONTEXT1}\n"  # Specified context
            f"{ARG1} {ARG2}"  # override args
        )
    ):
        InteractiveCommandAdder.edit_command(COMMAND1, empty_configuration)

    assert len(empty_configuration.commands_repository) == 1
    assert empty_configuration.commands_repository[COMMAND1] == CommandBuilder(
        name=COMMAND1,
        help=COMMAND_HELP_STRING1,
        contexts_specifications={context1: ContextSpecification(args=[ARG1, ARG2])},
    )


def test_interactive_edit_command_with_added_args_context(
    cli_runner, empty_configuration
):
    context1 = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    empty_configuration.contexts_repository.add_contexts(context1)
    empty_configuration.commands_repository.add_command_builders(
        CommandBuilder(name=COMMAND1, help=COMMAND_HELP_STRING1)
    )
    assert len(empty_configuration.commands_repository) == 1

    with cli_runner.isolation(
        input=(
            f"{COMMAND_HELP_STRING1}\n"  # help string
            "\n"  # no default args
            "\n"  # no version
            "\n"  # no required contexts
            "\n"  # no allowed contexts
            f"{CONTEXT1}\n"  # Specified context
            "\n"  # no override args
            f"{ARG1} {ARG2}"  # added args
        )
    ):
        InteractiveCommandAdder.edit_command(COMMAND1, empty_configuration)

    assert len(empty_configuration.commands_repository) == 1
    assert empty_configuration.commands_repository[COMMAND1] == CommandBuilder(
        name=COMMAND1,
        help=COMMAND_HELP_STRING1,
        contexts_specifications={context1: ContextSpecification(add_args=[ARG1, ARG2])},
    )


def test_interactive_edit_command_with_clear_args_context(
    cli_runner, empty_configuration
):
    context1 = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    empty_configuration.contexts_repository.add_contexts(context1)
    empty_configuration.commands_repository.add_command_builders(
        CommandBuilder(name=COMMAND1, help=COMMAND_HELP_STRING1)
    )
    assert len(empty_configuration.commands_repository) == 1

    with cli_runner.isolation(
        input=(
            f"{COMMAND_HELP_STRING1}\n"  # help string
            "\n"  # no default args
            "\n"  # no version
            "\n"  # no required contexts
            "\n"  # no allowed contexts
            f"{CONTEXT1}\n"  # Specified context
            "\n"  # no override args
            "\n"  # no override args
            "y\n"  # no override args
        )
    ):
        InteractiveCommandAdder.edit_command(COMMAND1, empty_configuration)

    assert len(empty_configuration.commands_repository) == 1
    assert empty_configuration.commands_repository[COMMAND1] == CommandBuilder(
        name=COMMAND1,
        help=COMMAND_HELP_STRING1,
        contexts_specifications={context1: ContextSpecification(clear_args=True)},
    )


def test_interactive_edit_command_with_both_added_args_and_override_context_fail(
    cli_runner, empty_configuration
):
    context1 = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    empty_configuration.contexts_repository.add_contexts(context1)
    empty_configuration.commands_repository.add_command_builders(
        CommandBuilder(name=COMMAND1, help=COMMAND_HELP_STRING1)
    )
    assert len(empty_configuration.commands_repository) == 1

    with cli_runner.isolation(
        input=(
            f"{COMMAND_HELP_STRING1}\n"  # help string
            "\n"  # no default args
            "\n"  # no version
            "\n"  # no required contexts
            "\n"  # no allowed contexts
            f"{CONTEXT1}\n"  # Specified context
            f"{ARG1} {ARG2}\n"  # override args
            f"{ARG3} {ARG4}\n"  # also added args, which will cause error
            "\n"  # no clear
            f"{ARG1} {ARG2}\n"  # ask again for override args
            "\n"  # no added args
            "\n"  # no clear
        )
    ):
        InteractiveCommandAdder.edit_command(COMMAND1, empty_configuration)

    assert len(empty_configuration.commands_repository) == 1
    assert empty_configuration.commands_repository[COMMAND1] == CommandBuilder(
        name=COMMAND1,
        help=COMMAND_HELP_STRING1,
        contexts_specifications={context1: ContextSpecification(args=[ARG1, ARG2])},
    )


def test_interactive_edit_command_re_ask_for_specified_context_due_to_unknown_context(
    cli_runner, empty_configuration
):
    context1, context2 = (
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
        Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2),
    )
    empty_configuration.contexts_repository.add_contexts(context1, context2)
    empty_configuration.commands_repository.add_command_builders(
        CommandBuilder(name=COMMAND1, help=COMMAND_HELP_STRING1)
    )
    assert len(empty_configuration.commands_repository) == 1

    with cli_runner.isolation(
        input=(
            f"{COMMAND_HELP_STRING1}\n"  # help string
            "\n"  # no default args
            "\n"  # no version
            "\n"  # no required contexts
            "\n"  # no allowed contexts
            f"{CONTEXT3}\n"  # nknown context
            f"{CONTEXT1}\n"  # specify context1 instead
            f"{ARG1} {ARG2}"  # override args
        )
    ):
        InteractiveCommandAdder.edit_command(COMMAND1, empty_configuration)

    assert len(empty_configuration.commands_repository) == 1
    assert empty_configuration.commands_repository[COMMAND1] == CommandBuilder(
        name=COMMAND1,
        help=COMMAND_HELP_STRING1,
        contexts_specifications={context1: ContextSpecification(args=[ARG1, ARG2])},
    )


def test_interactive_edit_command_re_ask_for_specified_context_due_to_taken_context(
    cli_runner, empty_configuration
):
    context1, context2, context3 = (
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
        Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2),
        Context(name=CONTEXT3, help=CONTEXT_HELP_STRING3),
    )
    empty_configuration.contexts_repository.add_contexts(context1, context2, context3)
    empty_configuration.commands_repository.add_command_builders(
        CommandBuilder(name=COMMAND1, help=COMMAND_HELP_STRING1)
    )
    assert len(empty_configuration.commands_repository) == 1

    with cli_runner.isolation(
        input=(
            f"{COMMAND_HELP_STRING1}\n"  # help string
            "\n"  # no default args
            "\n"  # no version
            f"{CONTEXT3}\n"  # required context
            "\n"  # no allowed contexts
            f"{CONTEXT3}\n"  # fail because context3 is already taken
            f"{CONTEXT1}\n"  # specify context1 instead
            f"{ARG1} {ARG2}"  # override args
        )
    ):
        InteractiveCommandAdder.edit_command(COMMAND1, empty_configuration)

    assert len(empty_configuration.commands_repository) == 1
    assert empty_configuration.commands_repository[COMMAND1] == CommandBuilder(
        name=COMMAND1,
        help=COMMAND_HELP_STRING1,
        required_contexts=[context3],
        contexts_specifications={context1: ContextSpecification(args=[ARG1, ARG2])},
    )
