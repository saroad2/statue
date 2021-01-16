import pytest
from pytest_cases import THIS_MODULE, parametrize_with_cases

from statue.command import Command
from statue.configuration import Configuration
from statue.constants import (
    ADD_ARGS,
    ARGS,
    CLEAR_ARGS,
    COMMANDS,
    CONTEXTS,
    HELP,
    STANDARD,
)
from statue.context import Context
from statue.exceptions import (
    InvalidCommand,
    MissingConfiguration,
    UnknownCommand,
    UnknownContext,
)
from tests.constants import (
    ARG1,
    ARG2,
    ARG3,
    ARG4,
    ARG5,
    COMMAND1,
    COMMAND2,
    COMMAND3,
    COMMAND_HELP_STRING1,
    COMMAND_HELP_STRING2,
    CONTEXT1,
    CONTEXT2,
    CONTEXT3,
    CONTEXT_HELP_STRING1,
    CONTEXT_HELP_STRING2,
    CONTEXTS_MAP,
    NOT_EXISTING_CONTEXT,
)

# Success cases
from tests.util import build_contexts_map


def case_success_with_no_contexts():
    configuration = {
        CONTEXTS: CONTEXTS_MAP,
        COMMANDS: {
            COMMAND1: {
                HELP: COMMAND_HELP_STRING1,
                ARGS: [ARG1],
                CONTEXT1: {ADD_ARGS: [ARG2, ARG3]},
                CONTEXT2: True,
            }
        },
    }
    kwargs = dict(command_name=COMMAND1)
    command = Command(name=COMMAND1, args=[ARG1], help=COMMAND_HELP_STRING1)
    return configuration, kwargs, command


def case_success_with_boolean_context():
    configuration = {
        CONTEXTS: CONTEXTS_MAP,
        COMMANDS: {
            COMMAND1: {
                HELP: COMMAND_HELP_STRING1,
                ARGS: [ARG1],
                CONTEXT1: True,
            }
        },
    }
    kwargs = dict(command_name=COMMAND1, contexts=[CONTEXT1])
    command = Command(name=COMMAND1, args=[ARG1], help=COMMAND_HELP_STRING1)
    return configuration, kwargs, command


def case_success_with_two_contexts():
    configuration = {
        CONTEXTS: CONTEXTS_MAP,
        COMMANDS: {
            COMMAND1: {
                HELP: COMMAND_HELP_STRING1,
                ARGS: [ARG1],
                CONTEXT1: True,
                CONTEXT2: True,
            }
        },
    }
    kwargs = dict(command_name=COMMAND1, contexts=[CONTEXT1, CONTEXT2])
    command = Command(name=COMMAND1, args=[ARG1], help=COMMAND_HELP_STRING1)
    return configuration, kwargs, command


def case_success_with_non_standard_command():
    configuration = {
        CONTEXTS: CONTEXTS_MAP,
        COMMANDS: {
            COMMAND1: {
                HELP: COMMAND_HELP_STRING1,
                ARGS: [ARG1],
                STANDARD: False,
                CONTEXT1: True,
            }
        },
    }
    kwargs = dict(command_name=COMMAND1, contexts=[CONTEXT1])
    command = Command(name=COMMAND1, args=[ARG1], help=COMMAND_HELP_STRING1)
    return configuration, kwargs, command


def case_success_with_override_context():
    configuration = {
        CONTEXTS: CONTEXTS_MAP,
        COMMANDS: {
            COMMAND1: {
                HELP: COMMAND_HELP_STRING1,
                ARGS: [ARG1, ARG2],
                CONTEXT1: {ARGS: [ARG3, ARG4]},
                CONTEXT2: {ARGS: [ARG5]},
            }
        },
    }
    kwargs = dict(command_name=COMMAND1, contexts=[CONTEXT1])
    command = Command(
        name=COMMAND1,
        args=[ARG3, ARG4],
        help=COMMAND_HELP_STRING1,
    )
    return configuration, kwargs, command


def case_success_with_clear_args_context():
    configuration = {
        CONTEXTS: CONTEXTS_MAP,
        COMMANDS: {
            COMMAND1: {
                HELP: COMMAND_HELP_STRING1,
                ARGS: [ARG1, ARG2],
                CONTEXT1: {CLEAR_ARGS: True},
                CONTEXT2: {ARGS: [ARG5]},
            }
        },
    }
    kwargs = dict(command_name=COMMAND1, contexts=[CONTEXT1])
    command = Command(name=COMMAND1, args=[], help=COMMAND_HELP_STRING1)
    return configuration, kwargs, command


def case_success_with_overrides_with_add_args_context():
    configuration = {
        CONTEXTS: CONTEXTS_MAP,
        COMMANDS: {
            COMMAND1: {
                HELP: COMMAND_HELP_STRING1,
                ARGS: [ARG1, ARG2],
                CONTEXT1: {ADD_ARGS: [ARG3, ARG4]},
                CONTEXT2: {ARGS: [ARG5]},
            }
        },
    }
    kwargs = dict(command_name=COMMAND1, contexts=[CONTEXT1])
    command = Command(
        name=COMMAND1,
        args=[ARG1, ARG2, ARG3, ARG4],
        help=COMMAND_HELP_STRING1,
    )
    return configuration, kwargs, command


def case_success_with_empty_allow_list():
    configuration = {
        CONTEXTS: CONTEXTS_MAP,
        COMMANDS: {COMMAND1: {HELP: COMMAND_HELP_STRING1, ARGS: [ARG1, ARG2]}},
    }
    kwargs = dict(command_name=COMMAND1, allow_list=[])
    command = Command(name=COMMAND1, args=[ARG1, ARG2], help=COMMAND_HELP_STRING1)
    return configuration, kwargs, command


def case_success_in_allow_list():
    configuration = {
        CONTEXTS: CONTEXTS_MAP,
        COMMANDS: {COMMAND1: {HELP: COMMAND_HELP_STRING1, ARGS: [ARG1, ARG2]}},
    }
    kwargs = dict(command_name=COMMAND1, allow_list=[COMMAND1])
    command = Command(name=COMMAND1, args=[ARG1, ARG2], help=COMMAND_HELP_STRING1)
    return configuration, kwargs, command


def case_success_not_in_deny_list():
    configuration = {
        CONTEXTS: CONTEXTS_MAP,
        COMMANDS: {
            COMMAND1: {HELP: COMMAND_HELP_STRING1, ARGS: [ARG1, ARG2]},
            COMMAND2: {HELP: COMMAND_HELP_STRING2, ARGS: [ARG3]},
        },
    }
    kwargs = dict(command_name=COMMAND1, deny_list=[COMMAND2])
    command = Command(name=COMMAND1, args=[ARG1, ARG2], help=COMMAND_HELP_STRING1)
    return configuration, kwargs, command


def case_success_on_root_context_inheritance():
    standard = Context(name=STANDARD, help="Some help", is_default=True)
    parent = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    context = Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2, parent=parent)
    configuration = {
        CONTEXTS: build_contexts_map(standard, context, parent),
        COMMANDS: {
            COMMAND1: {
                HELP: COMMAND_HELP_STRING1,
                ARGS: [ARG1, ARG2],
                CONTEXT1: {ARGS: [ARG3]},
            },
        },
    }
    kwargs = dict(command_name=COMMAND1)
    command = Command(name=COMMAND1, args=[ARG1, ARG2], help=COMMAND_HELP_STRING1)
    return configuration, kwargs, command


def case_success_on_child_context_inheritance():
    parent = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1)
    context = Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2, parent=parent)
    configuration = {
        CONTEXTS: build_contexts_map(parent, context),
        COMMANDS: {
            COMMAND1: {
                HELP: COMMAND_HELP_STRING1,
                ARGS: [ARG1, ARG2],
                CONTEXT1: {ARGS: [ARG3]},
            },
        },
    }
    kwargs = dict(command_name=COMMAND1, contexts=[CONTEXT2])
    command = Command(name=COMMAND1, args=[ARG3], help=COMMAND_HELP_STRING1)
    return configuration, kwargs, command


def case_success_on_standard_child_context_inheritance():
    standard = Context(name=STANDARD, help=CONTEXT_HELP_STRING2, is_default=True)
    context = Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1, parent=standard)
    configuration = {
        CONTEXTS: build_contexts_map(standard, context),
        COMMANDS: {
            COMMAND1: {
                HELP: COMMAND_HELP_STRING1,
                ARGS: [ARG1, ARG2],
            },
        },
    }
    kwargs = dict(command_name=COMMAND1, contexts=[CONTEXT1])
    command = Command(name=COMMAND1, args=[ARG1, ARG2], help=COMMAND_HELP_STRING1)
    return configuration, kwargs, command


@parametrize_with_cases(
    argnames="configuration, kwargs, command",
    cases=THIS_MODULE,
    prefix="case_success_",
)
def test_read_command_success(configuration, kwargs, command, clear_configuration):
    Configuration.set_statue_configuration(configuration)
    actual_command = Configuration.read_command(**kwargs)
    assert actual_command == command, "Command is different than exp expected"


# Failure cases


def case_failure_with_non_existing_context():
    configuration = {
        CONTEXTS: CONTEXTS_MAP,
        COMMANDS: {
            COMMAND1: {
                HELP: COMMAND_HELP_STRING1,
                ARGS: [ARG1],
                CONTEXT1: {ADD_ARGS: [ARG2, ARG3]},
            }
        },
    }
    kwargs = dict(command_name=COMMAND1, contexts=[NOT_EXISTING_CONTEXT])
    return (
        configuration,
        kwargs,
        UnknownContext,
        f'^Could not find context named "{NOT_EXISTING_CONTEXT}".$',
    )


def case_failure_with_two_contexts():
    configuration = {
        CONTEXTS: CONTEXTS_MAP,
        COMMANDS: {
            COMMAND1: {
                HELP: COMMAND_HELP_STRING1,
                ARGS: [ARG1],
                CONTEXT1: True,
            }
        },
    }
    kwargs = dict(command_name=COMMAND1, contexts=[CONTEXT1, CONTEXT2])
    return (
        configuration,
        kwargs,
        InvalidCommand,
        (
            f'^The command "{COMMAND1}" does not match the restrictions: '
            fr"contexts=\['{CONTEXT1}', '{CONTEXT2}'\], allow_list=None, "
            "deny_list=None$"
        ),
    )


def case_failure_with_non_standard_command():
    configuration = {
        CONTEXTS: CONTEXTS_MAP,
        COMMANDS: {
            COMMAND1: {
                HELP: COMMAND_HELP_STRING1,
                ARGS: [ARG1],
                STANDARD: False,
                CONTEXT1: True,
            }
        },
    }
    kwargs = dict(command_name=COMMAND1)
    return (
        configuration,
        kwargs,
        InvalidCommand,
        (
            f'^The command "{COMMAND1}" does not match the restrictions: '
            "contexts=None, allow_list=None, deny_list=None$"
        ),
    )


def case_failure_not_in_allow_list():
    configuration = {
        CONTEXTS: CONTEXTS_MAP,
        COMMANDS: {
            COMMAND1: {HELP: COMMAND_HELP_STRING1, ARGS: [ARG1, ARG2]},
            COMMAND2: {HELP: COMMAND_HELP_STRING2, ARGS: [ARG3]},
        },
    }
    kwargs = dict(command_name=COMMAND1, allow_list=[COMMAND2])
    return (
        configuration,
        kwargs,
        InvalidCommand,
        (
            f'^The command "{COMMAND1}" does not match the restrictions: '
            fr"contexts=None, allow_list=\['{COMMAND2}'\], deny_list=None$"
        ),
    )


def case_failure_in_deny_list():
    configuration = {
        CONTEXTS: CONTEXTS_MAP,
        COMMANDS: {
            COMMAND1: {HELP: COMMAND_HELP_STRING1, ARGS: [ARG1, ARG2]},
            COMMAND2: {HELP: COMMAND_HELP_STRING2, ARGS: [ARG3, ARG4]},
        },
    }
    kwargs = dict(command_name=COMMAND1, deny_list=[COMMAND1])
    return (
        configuration,
        kwargs,
        InvalidCommand,
        (
            f'^The command "{COMMAND1}" does not match the restrictions: '
            fr"contexts=None, allow_list=None, deny_list=\['{COMMAND1}'\]$"
        ),
    )


def case_failure_non_existing_command():
    configuration = {
        CONTEXTS: CONTEXTS_MAP,
        COMMANDS: {
            COMMAND1: {HELP: COMMAND_HELP_STRING1, ARGS: [ARG1, ARG2]},
            COMMAND2: {HELP: COMMAND_HELP_STRING2, ARGS: [ARG3, ARG5]},
        },
    }
    kwargs = dict(command_name=COMMAND3)
    return (
        configuration,
        kwargs,
        UnknownCommand,
        f'^Could not find command named "{COMMAND3}".$',
    )


def case_failure_with_no_commands_configuration():
    configuration = {CONTEXTS: CONTEXTS_MAP}
    kwargs = dict(command_name=COMMAND3)
    return (
        configuration,
        kwargs,
        MissingConfiguration,
        f'^"{COMMANDS}" is missing from Statue configuration.$',
    )


def case_failure_when_no_context_configuration_was_set():
    configuration = {
        COMMANDS: {
            COMMAND1: {HELP: COMMAND_HELP_STRING1, ARGS: [ARG1, ARG2], CONTEXT1: True},
            COMMAND2: {HELP: COMMAND_HELP_STRING2, ARGS: [ARG3, ARG5]},
        },
    }
    kwargs = dict(command_name=COMMAND1, contexts=[CONTEXT1])
    return (
        configuration,
        kwargs,
        MissingConfiguration,
        f'^"{CONTEXTS}" is missing from Statue configuration.$',
    )


@parametrize_with_cases(
    argnames="configuration, kwargs, exception_class, exception_message",
    cases=THIS_MODULE,
    prefix="case_failure_",
)
def test_read_command_failure(
    configuration, kwargs, exception_class, exception_message, clear_configuration
):
    Configuration.set_statue_configuration(configuration)
    with pytest.raises(expected_exception=exception_class, match=exception_message):
        Configuration.read_command(**kwargs)


# Additional tests


def test_read_command_multiple_times(
    clear_configuration,
):
    Configuration.set_statue_configuration(
        {
            CONTEXTS: CONTEXTS_MAP,
            COMMANDS: {
                COMMAND1: {
                    HELP: COMMAND_HELP_STRING1,
                    ARGS: [ARG1],
                    CONTEXT1: {ADD_ARGS: [ARG2, ARG3]},
                    CONTEXT2: {CLEAR_ARGS: True},
                    CONTEXT3: {ARGS: [ARG5]},
                }
            },
        }
    )
    command1 = Configuration.read_command(command_name=COMMAND1, contexts=[CONTEXT1])
    assert command1 == Command(
        name=COMMAND1, help=COMMAND_HELP_STRING1, args=[ARG1, ARG2, ARG3]
    ), "Command is different than expected in first read."

    command2 = Configuration.read_command(command_name=COMMAND1)
    assert command2 == Command(
        name=COMMAND1, help=COMMAND_HELP_STRING1, args=[ARG1]
    ), "Command is different than expected in second read."

    command3 = Configuration.read_command(command_name=COMMAND1, contexts=[CONTEXT2])
    assert command3 == Command(
        name=COMMAND1, help=COMMAND_HELP_STRING1, args=[]
    ), "Command is different than expected in forth read."

    command4 = Configuration.read_command(command_name=COMMAND1, contexts=[CONTEXT3])
    assert command4 == Command(
        name=COMMAND1, help=COMMAND_HELP_STRING1, args=[ARG5]
    ), "Command is different than expected in third read."
