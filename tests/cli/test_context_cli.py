# from statue.cli import statue as statue_cli
# from tests.constants import (
#     COMMAND1,
#     COMMAND2,
#     CONTEXT1,
#     CONTEXT2,
#     CONTEXT3,
#     CONTEXT4,
#     CONTEXT_HELP_STRING1,
#     CONTEXT_HELP_STRING2,
#     CONTEXT_HELP_STRING3,
#     CONTEXT_HELP_STRING4,
#     NOT_EXISTING_CONTEXT,
# )
#
#
# def test_contexts_list_of_full_configuration(cli_runner, full_configuration):
#     result = cli_runner.invoke(statue_cli, ["context", "list"])
#     assert result.exit_code == 0, "list contexts should exit with success."
#     assert result.output == (
#         f"{CONTEXT1} - {CONTEXT_HELP_STRING1}\n"
#         f"{CONTEXT2} - {CONTEXT_HELP_STRING2}\n"
#         f"{CONTEXT3} - {CONTEXT_HELP_STRING3}\n"
#         f"{CONTEXT4} - {CONTEXT_HELP_STRING4}\n"
#     ), "List output is different than expected."
#
#
# def test_contexts_list_of_an_empty_configuration(cli_runner, empty_configuration):
#     result = cli_runner.invoke(statue_cli, ["context", "list"])
#     assert result.exit_code == 1, "list contexts should exit with failure."
#     assert (
#         result.output == "No contexts were found.\n"
#     ), "List output is different than expected."
#
#
# def test_contexts_show_of_existing_context(cli_runner, full_configuration):
#     result = cli_runner.invoke(statue_cli, ["context", "show", CONTEXT2])
#     assert result.exit_code == 0, "show context should exit with success."
#     assert result.output == (
#         f"Name - {CONTEXT2}\n"
#         f"Description - {CONTEXT_HELP_STRING2}\n"
#         f"Matching commands - {COMMAND1}, {COMMAND2}\n"
#     ), "Show output is different than expected."
#
#
# def test_contexts_show_of_empty_configuration(cli_runner, empty_configuration):
#     result = cli_runner.invoke(statue_cli, ["context", "show", CONTEXT2])
#     assert result.exit_code == 1, "show context should exit with failure."
#     assert (
#         result.output == "No contexts were found.\n"
#     ), "Show output is different than expected."
#
#
# def test_contexts_show_of_non_existing_context(cli_runner, full_configuration):
#     result = cli_runner.invoke(statue_cli, ["context", "show", NOT_EXISTING_CONTEXT])
#     assert result.exit_code == 1, "show context should exit with failure."
#     assert (
#         result.output == f'Could not find the context "{NOT_EXISTING_CONTEXT}".\n'
#     ), "Show output is different than expected."
