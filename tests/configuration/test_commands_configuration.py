from statue.configuration import Configuration
from statue.constants import COMMANDS
from tests.constants import (
    COMMAND1,
    COMMAND2,
    COMMAND3,
    COMMAND4,
    COMMAND5,
    COMMANDS_CONFIGURATION,
)


def test_simple_commands_configuration(clear_configuration):
    Configuration.set_statue_configuration({COMMANDS: COMMANDS_CONFIGURATION})
    assert (
        Configuration.commands_configuration() == COMMANDS_CONFIGURATION
    ), "Commands configuration is different than expected"
    assert Configuration.commands_names_list() == [
        COMMAND1,
        COMMAND2,
        COMMAND3,
        COMMAND4,
        COMMAND5,
    ], "Commands names list is different than expected"


def test_empty_commands_configuration(clear_configuration):
    Configuration.set_statue_configuration({})
    assert (
        Configuration.commands_configuration() is None
    ), "Commands configuration is different than expected"
    assert (
        not Configuration.commands_names_list()
    ), "Commands names list is different than expected"
