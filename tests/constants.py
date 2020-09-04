from statue.constants import ADD_ARGS, ARGS, CLEAR_ARGS, HELP, PARENT, STANDARD


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
NOT_EXISTING_COMMAND = "not_existing_command"
ENCODING = "utf8"


CONTEXTS_CONFIGURATION = {
    CONTEXT1: {HELP: CONTEXT_HELP_STRING1},
    CONTEXT2: {HELP: CONTEXT_HELP_STRING2},
    CONTEXT3: {HELP: CONTEXT_HELP_STRING3},
    CONTEXT4: {HELP: CONTEXT_HELP_STRING4},
}
