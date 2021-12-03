from statue.constants import HELP, STANDARD
from statue.context import Context

SUCCESSFUL_TAG = "successful"
FAILED_TAG = "failed"


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
COMMAND6, COMMAND_HELP_STRING6 = name_and_help_string("command6")
ARG1, ARG2, ARG3, ARG4, ARG5 = "arg1", "arg2", "arg3", "arg4", "arg5"
VERSION1 = "version1"
CONTEXT1, CONTEXT_HELP_STRING1 = name_and_help_string("context1")
CONTEXT2, CONTEXT_HELP_STRING2 = name_and_help_string("context2")
CONTEXT3, CONTEXT_HELP_STRING3 = name_and_help_string("context3")
CONTEXT4, CONTEXT_HELP_STRING4 = name_and_help_string("context4")
CONTEXT5, CONTEXT_HELP_STRING5 = name_and_help_string("context5")
NOT_EXISTING_CONTEXT = "not_existing_context"
NOT_EXISTING_COMMAND = "not_existing_command"
NOT_EXISTING_SOURCE = "not_existing_source"
ENCODING = "utf8"

COMMANDS_CONFIGURATION = {
    COMMAND1: {HELP: COMMAND_HELP_STRING1},
    COMMAND2: {HELP: COMMAND_HELP_STRING2},
    COMMAND3: {HELP: COMMAND_HELP_STRING3},
    COMMAND4: {HELP: COMMAND_HELP_STRING4},
    COMMAND5: {HELP: COMMAND_HELP_STRING5},
}

STANDARD_HELP = "Standard help"
CONTEXTS_MAP = {
    STANDARD: Context(name=STANDARD, help=STANDARD_HELP, is_default=True),
    CONTEXT1: Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
    CONTEXT2: Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2),
    CONTEXT3: Context(name=CONTEXT3, help=CONTEXT_HELP_STRING3),
    CONTEXT4: Context(name=CONTEXT4, help=CONTEXT_HELP_STRING4),
    CONTEXT5: Context(name=CONTEXT5, help=CONTEXT_HELP_STRING5),
}
