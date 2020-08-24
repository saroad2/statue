import pytest

from statue.constants import ADD_ARGS, ARGS, CLEAR_ARGS, HELP, STANDARD


def name_and_help_string(name):
    return name, f"This is a help string for {name}"


SOURCE1, SOURCE2, SOURCE3, SOURCE4, SOURCE5 = (
    "source1",
    "source2",
    "source3",
    "source4",
    "source5",
)
COMMAND1, COMMAND_HELP_STRING1 = name_and_help_string("command1")
COMMAND2, COMMAND_HELP_STRING2 = name_and_help_string("command2")
COMMAND3, COMMAND_HELP_STRING3 = name_and_help_string("command3")
COMMAND4, COMMAND_HELP_STRING4 = name_and_help_string("command4")
COMMAND5, COMMAND_HELP_STRING5 = name_and_help_string("command5")
ARG1, ARG2, ARG3, ARG4, ARG5 = "arg1", "arg2", "arg3", "arg4", "arg5"
CONTEXT1, CONTEXT_HELP_STRING1 = name_and_help_string("context1")
CONTEXT2, CONTEXT_HELP_STRING2 = name_and_help_string("context2")
CONTEXT3, CONTEXT_HELP_STRING3 = name_and_help_string("context3")
CONTEXT4, CONTEXT_HELP_STRING4 = name_and_help_string("context4")
NOT_EXISTING_CONTEXT = "not_existing_context"
ENCODING = "utf8"


@pytest.fixture
def empty_settings():
    return {}


@pytest.fixture
def non_empty_sources_config():
    return dict(
        contexts={},
        commands={},
        sources={
            SOURCE1: {},
            SOURCE2: dict(contexts=[CONTEXT1]),
            SOURCE3: dict(contexts=[CONTEXT2]),
            SOURCE4: dict(allow_list=[COMMAND1, COMMAND3, COMMAND4]),
            SOURCE5: dict(deny_list=[COMMAND5]),
        },
    )


@pytest.fixture
def one_command_setting():
    return {COMMAND1: {HELP: COMMAND_HELP_STRING1}}


@pytest.fixture
def one_command_with_args_settings():
    return {COMMAND1: {HELP: COMMAND_HELP_STRING1, ARGS: [ARG1, ARG2]}}


@pytest.fixture
def full_commands_settings_with_boolean_contexts():
    return {
        COMMAND1: {
            HELP: COMMAND_HELP_STRING1,
            ARGS: [ARG1, ARG2],
            CONTEXT1: True,
            CONTEXT2: True,
        },
        COMMAND2: {HELP: COMMAND_HELP_STRING2, ARGS: [ARG3], CONTEXT2: True},
        COMMAND3: {HELP: COMMAND_HELP_STRING3, CONTEXT3: True},
        COMMAND4: {HELP: COMMAND_HELP_STRING4, ARGS: [ARG4, ARG5]},
        COMMAND5: {HELP: COMMAND_HELP_STRING5, STANDARD: False, CONTEXT4: True},
    }


@pytest.fixture
def full_commands_settings():
    return {
        COMMAND1: {
            HELP: COMMAND_HELP_STRING1,
            ARGS: [ARG1, ARG2],
            CONTEXT1: {ARGS: [ARG3]},
            CONTEXT2: {ARGS: [ARG4, ARG5]},
            CONTEXT3: {CLEAR_ARGS: True},
            CONTEXT4: {ADD_ARGS: [ARG5]},
        },
        COMMAND2: {
            HELP: COMMAND_HELP_STRING2,
            ARGS: [],
            STANDARD: False,
            CONTEXT2: {ADD_ARGS: [ARG3, ARG5]},
            CONTEXT4: True,
        },
    }


@pytest.fixture
def full_contexts_settings():
    return {
        CONTEXT1: CONTEXT_HELP_STRING1,
        CONTEXT2: CONTEXT_HELP_STRING2,
        CONTEXT3: CONTEXT_HELP_STRING3,
        CONTEXT4: CONTEXT_HELP_STRING4,
    }
