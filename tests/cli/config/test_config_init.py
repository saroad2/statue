import git
import mock
import pytest

from statue.cli import statue_cli
from statue.cli.config.interactive_adders.interactive_sources_adder import (
    InteractiveSourcesAdder,
)
from statue.commands_filter import CommandsFilter
from statue.config.configuration import Configuration
from statue.context import Context
from statue.exceptions import StatueConfigurationError, UnknownTemplate
from tests.constants import (
    CONTEXT1,
    CONTEXT2,
    CONTEXT3,
    CONTEXT_HELP_STRING1,
    CONTEXT_HELP_STRING2,
    CONTEXT_HELP_STRING3,
    SOURCE1,
    SOURCE2,
    SOURCE3,
)
from tests.util import command_builder_mock, dummy_version


@pytest.fixture
def mock_git_repo(mocker):
    return mocker.patch("git.Repo")


@pytest.fixture
def mock_update_sources_repository(mocker):
    return mocker.patch.object(InteractiveSourcesAdder, "update_sources_repository")


def dummy_configuration():
    configuration = Configuration(cache=mock.Mock())
    configuration.contexts_repository.add_contexts(
        Context(name=CONTEXT1, help=CONTEXT_HELP_STRING1),
        Context(name=CONTEXT2, help=CONTEXT_HELP_STRING2),
        Context(name=CONTEXT3, help=CONTEXT_HELP_STRING3),
    )
    configuration.commands_repository.add_command_builders(
        command_builder_mock(name=CONTEXT1, installed_version=dummy_version()),
        command_builder_mock(name=CONTEXT2, installed_version=dummy_version()),
        command_builder_mock(name=CONTEXT3, installed_version=dummy_version()),
    )
    configuration.to_toml = mock.Mock()
    return configuration


def test_config_init_blank(
    cli_runner,
    mock_configuration_path,
    mock_build_configuration_from_file,
    mock_templates_provider_get_template_path,
    mock_git_repo,
    mock_update_sources_repository,
    mock_configuration_as_dict,
):
    with mock.patch.object(
        Configuration, "empty_configuration"
    ) as empty_configuration_mock:
        result = cli_runner.invoke(statue_cli, ["config", "init", "--blank"])
        empty_configuration_mock.assert_called_once_with()
        empty_configuration_mock.return_value.to_toml.assert_called_once_with(
            mock_configuration_path.return_value
        )

    assert result.exit_code == 0, f"Exited with exception: {result.exception}"
    mock_configuration_path.assert_called_once_with()
    mock_git_repo.assert_not_called()
    mock_templates_provider_get_template_path.assert_not_called()
    mock_build_configuration_from_file.assert_not_called()

    mock_update_sources_repository.assert_not_called()


def test_config_init_all_yes(
    cli_runner,
    mock_configuration_path,
    mock_build_configuration_from_file,
    mock_templates_provider_get_template_path,
    mock_git_repo,
    mock_cwd,
    mock_update_sources_repository,
    mock_configuration_as_dict,
):
    source_path1, source_path2, source_path3 = (
        mock_cwd / f"{SOURCE1}.py",
        mock_cwd / f"{SOURCE2}.py",
        mock_cwd / f"{SOURCE3}.py",
    )
    source_path1.touch()
    source_path2.touch()
    source_path3.touch()
    mock_build_configuration_from_file.return_value = (
        configuration
    ) = dummy_configuration()
    result = cli_runner.invoke(statue_cli, ["config", "init", "-y"])

    assert result.exit_code == 0, f"Exited with exception: {result.exception}"
    mock_configuration_path.assert_called_once_with()
    mock_git_repo.assert_called_once_with(mock_cwd)
    mock_templates_provider_get_template_path.assert_called_once_with("defaults")
    mock_build_configuration_from_file.assert_called_once_with(
        mock_templates_provider_get_template_path.return_value
    )
    assert len(configuration.sources_repository) == 3
    assert configuration.sources_repository[source_path1] == CommandsFilter()
    assert configuration.sources_repository[source_path2] == CommandsFilter()
    assert configuration.sources_repository[source_path3] == CommandsFilter()

    assert len(configuration.commands_repository) == 3
    for command_builder in configuration.commands_repository:
        command_builder.update.assert_not_called()
        assert command_builder.version is None

    mock_update_sources_repository.assert_not_called()
    configuration.to_toml.assert_called_once_with(mock_configuration_path.return_value)


def test_config_init_interactive(
    cli_runner,
    mock_configuration_path,
    mock_build_configuration_from_file,
    mock_templates_provider_get_template_path,
    mock_git_repo,
    mock_cwd,
    mock_update_sources_repository,
    mock_configuration_as_dict,
):
    source_path1, source_path2, source_path3 = (
        mock_cwd / f"{SOURCE1}.py",
        mock_cwd / f"{SOURCE2}.py",
        mock_cwd / f"{SOURCE3}.py",
    )
    source_path1.touch()
    source_path2.touch()
    source_path3.touch()
    mock_build_configuration_from_file.return_value = (
        configuration
    ) = dummy_configuration()

    result = cli_runner.invoke(statue_cli, ["config", "init"])

    assert result.exit_code == 0, f"Exited with exception: {result.exception}"
    mock_configuration_path.assert_called_once_with()
    mock_git_repo.assert_called_once_with(mock_cwd)
    mock_templates_provider_get_template_path.assert_called_once_with("defaults")
    mock_build_configuration_from_file.assert_called_once_with(
        mock_templates_provider_get_template_path.return_value
    )
    mock_update_sources_repository.assert_called_once_with(
        configuration=configuration,
        sources=[
            source_path1.relative_to(mock_cwd),
            source_path2.relative_to(mock_cwd),
            source_path3.relative_to(mock_cwd),
        ],
        repo=mock_git_repo.return_value,
        exclude=(),
    )
    configuration.to_toml.assert_called_once_with(mock_configuration_path.return_value)

    assert len(configuration.commands_repository) == 3
    for command_builder in configuration.commands_repository:
        command_builder.update.assert_not_called()
        assert command_builder.version is None


def test_config_init_all_yes_without_git(
    cli_runner,
    mock_configuration_path,
    mock_build_configuration_from_file,
    mock_templates_provider_get_template_path,
    mock_git_repo,
    mock_cwd,
    mock_update_sources_repository,
    mock_configuration_as_dict,
):
    source_path1, source_path2, source_path3 = (
        mock_cwd / f"{SOURCE1}.py",
        mock_cwd / f"{SOURCE2}.py",
        mock_cwd / f"{SOURCE3}.py",
    )
    source_path1.touch()
    source_path2.touch()
    source_path3.touch()
    mock_build_configuration_from_file.return_value = (
        configuration
    ) = dummy_configuration()

    result = cli_runner.invoke(statue_cli, ["config", "init", "-y", "--no-git"])

    assert result.exit_code == 0, f"Exited with exception: {result.exception}"
    mock_configuration_path.assert_called_once_with()
    mock_git_repo.assert_not_called()
    mock_templates_provider_get_template_path.assert_called_once_with("defaults")
    mock_build_configuration_from_file.assert_called_once_with(
        mock_templates_provider_get_template_path.return_value
    )
    assert len(configuration.sources_repository) == 3
    assert configuration.sources_repository[source_path1] == CommandsFilter()
    assert configuration.sources_repository[source_path2] == CommandsFilter()
    assert configuration.sources_repository[source_path3] == CommandsFilter()

    assert len(configuration.commands_repository) == 3
    for command_builder in configuration.commands_repository:
        command_builder.update.assert_not_called()
        assert command_builder.version is None

    mock_update_sources_repository.assert_not_called()
    configuration.to_toml.assert_called_once_with(mock_configuration_path.return_value)


def test_config_init_interactive_without_git(
    cli_runner,
    mock_configuration_path,
    mock_build_configuration_from_file,
    mock_templates_provider_get_template_path,
    mock_git_repo,
    mock_cwd,
    mock_update_sources_repository,
    mock_configuration_as_dict,
):
    source_path1, source_path2, source_path3 = (
        mock_cwd / f"{SOURCE1}.py",
        mock_cwd / f"{SOURCE2}.py",
        mock_cwd / f"{SOURCE3}.py",
    )
    source_path1.touch()
    source_path2.touch()
    source_path3.touch()
    mock_build_configuration_from_file.return_value = (
        configuration
    ) = dummy_configuration()

    result = cli_runner.invoke(statue_cli, ["config", "init", "--no-git"])

    assert result.exit_code == 0, f"Exited with exception: {result.exception}"
    mock_configuration_path.assert_called_once_with()
    mock_git_repo.assert_not_called()
    mock_templates_provider_get_template_path.assert_called_once_with("defaults")
    mock_build_configuration_from_file.assert_called_once_with(
        mock_templates_provider_get_template_path.return_value
    )
    mock_update_sources_repository.assert_called_once_with(
        configuration=configuration,
        sources=[
            source_path1.relative_to(mock_cwd),
            source_path2.relative_to(mock_cwd),
            source_path3.relative_to(mock_cwd),
        ],
        repo=None,
        exclude=(),
    )
    configuration.to_toml.assert_called_once_with(mock_configuration_path.return_value)

    assert len(configuration.commands_repository) == 3
    for command_builder in configuration.commands_repository:
        command_builder.update.assert_not_called()
        assert command_builder.version is None


def test_config_init_all_yes_with_git_raises_exception(
    cli_runner,
    mock_configuration_path,
    mock_build_configuration_from_file,
    mock_templates_provider_get_template_path,
    mock_git_repo,
    mock_cwd,
    mock_update_sources_repository,
    mock_configuration_as_dict,
):
    source_path1, source_path2, source_path3 = (
        mock_cwd / f"{SOURCE1}.py",
        mock_cwd / f"{SOURCE2}.py",
        mock_cwd / f"{SOURCE3}.py",
    )
    source_path1.touch()
    source_path2.touch()
    source_path3.touch()
    mock_git_repo.side_effect = git.InvalidGitRepositoryError
    mock_build_configuration_from_file.return_value = (
        configuration
    ) = dummy_configuration()

    result = cli_runner.invoke(statue_cli, ["config", "init", "-y"])

    assert result.exit_code == 0, f"Exited with exception: {result.exception}"
    mock_configuration_path.assert_called_once_with()
    mock_git_repo.assert_called_once_with(mock_cwd)
    mock_templates_provider_get_template_path.assert_called_once_with("defaults")
    mock_build_configuration_from_file.assert_called_once_with(
        mock_templates_provider_get_template_path.return_value
    )
    assert len(configuration.sources_repository) == 3
    assert configuration.sources_repository[source_path1] == CommandsFilter()
    assert configuration.sources_repository[source_path2] == CommandsFilter()
    assert configuration.sources_repository[source_path3] == CommandsFilter()

    assert len(configuration.commands_repository) == 3
    for command_builder in configuration.commands_repository:
        command_builder.update.assert_not_called()
        assert command_builder.version is None

    mock_update_sources_repository.assert_not_called()
    configuration.to_toml.assert_called_once_with(mock_configuration_path.return_value)


def test_config_init_interactive_with_git_raises_exception(
    cli_runner,
    mock_configuration_path,
    mock_build_configuration_from_file,
    mock_templates_provider_get_template_path,
    mock_git_repo,
    mock_cwd,
    mock_update_sources_repository,
    mock_configuration_as_dict,
):
    source_path1, source_path2, source_path3 = (
        mock_cwd / f"{SOURCE1}.py",
        mock_cwd / f"{SOURCE2}.py",
        mock_cwd / f"{SOURCE3}.py",
    )
    source_path1.touch()
    source_path2.touch()
    source_path3.touch()
    mock_git_repo.side_effect = git.InvalidGitRepositoryError
    mock_build_configuration_from_file.return_value = (
        configuration
    ) = dummy_configuration()

    result = cli_runner.invoke(statue_cli, ["config", "init"])

    assert result.exit_code == 0, f"Exited with exception: {result.exception}"
    mock_configuration_path.assert_called_once_with()
    mock_git_repo.assert_called_once_with(mock_cwd)
    mock_templates_provider_get_template_path.assert_called_once_with("defaults")
    mock_build_configuration_from_file.assert_called_once_with(
        mock_templates_provider_get_template_path.return_value
    )
    mock_update_sources_repository.assert_called_once_with(
        configuration=configuration,
        sources=[
            source_path1.relative_to(mock_cwd),
            source_path2.relative_to(mock_cwd),
            source_path3.relative_to(mock_cwd),
        ],
        repo=None,
        exclude=(),
    )
    configuration.to_toml.assert_called_once_with(mock_configuration_path.return_value)

    assert len(configuration.commands_repository) == 3
    for command_builder in configuration.commands_repository:
        command_builder.update.assert_not_called()
        assert command_builder.version is None


def test_config_init_interactive_with_template_name(
    cli_runner,
    mock_configuration_path,
    mock_build_configuration_from_file,
    mock_templates_provider_get_template_path,
    mock_git_repo,
    mock_cwd,
    mock_update_sources_repository,
    mock_configuration_as_dict,
):
    source_path1, source_path2, source_path3 = (
        mock_cwd / f"{SOURCE1}.py",
        mock_cwd / f"{SOURCE2}.py",
        mock_cwd / f"{SOURCE3}.py",
    )
    source_path1.touch()
    source_path2.touch()
    source_path3.touch()
    template_name = "template"
    mock_build_configuration_from_file.return_value = (
        configuration
    ) = dummy_configuration()

    result = cli_runner.invoke(statue_cli, ["config", "init", "-t", template_name])

    assert result.exit_code == 0, f"Exited with exception: {result.exception}"
    mock_configuration_path.assert_called_once_with()
    mock_git_repo.assert_called_once_with(mock_cwd)
    mock_templates_provider_get_template_path.assert_called_once_with(template_name)
    mock_build_configuration_from_file.assert_called_once_with(
        mock_templates_provider_get_template_path.return_value
    )
    mock_update_sources_repository.assert_called_once_with(
        configuration=configuration,
        sources=[
            source_path1.relative_to(mock_cwd),
            source_path2.relative_to(mock_cwd),
            source_path3.relative_to(mock_cwd),
        ],
        repo=mock_git_repo.return_value,
        exclude=(),
    )
    configuration.to_toml.assert_called_once_with(mock_configuration_path.return_value)

    assert len(configuration.commands_repository) == 3
    for command_builder in configuration.commands_repository:
        command_builder.update.assert_not_called()
        assert command_builder.version is None


@pytest.mark.parametrize(argnames="install_flag", argvalues=["-i", "--install"])
def test_config_init_with_install(
    install_flag,
    cli_runner,
    mock_configuration_path,
    mock_build_configuration_from_file,
    mock_templates_provider_get_template_path,
    mock_git_repo,
    mock_cwd,
    mock_update_sources_repository,
    mock_configuration_as_dict,
):
    source_path1, source_path2, source_path3 = (
        mock_cwd / f"{SOURCE1}.py",
        mock_cwd / f"{SOURCE2}.py",
        mock_cwd / f"{SOURCE3}.py",
    )
    source_path1.touch()
    source_path2.touch()
    source_path3.touch()
    mock_build_configuration_from_file.return_value = (
        configuration
    ) = dummy_configuration()

    result = cli_runner.invoke(statue_cli, ["config", "init", install_flag])

    assert result.exit_code == 0, f"Exited with exception: {result.exception}"
    mock_configuration_path.assert_called_once_with()
    mock_git_repo.assert_called_once_with(mock_cwd)
    mock_templates_provider_get_template_path.assert_called_once_with("defaults")
    mock_build_configuration_from_file.assert_called_once_with(
        mock_templates_provider_get_template_path.return_value
    )
    mock_update_sources_repository.assert_called_once_with(
        configuration=configuration,
        sources=[
            source_path1.relative_to(mock_cwd),
            source_path2.relative_to(mock_cwd),
            source_path3.relative_to(mock_cwd),
        ],
        repo=mock_git_repo.return_value,
        exclude=(),
    )
    configuration.to_toml.assert_called_once_with(mock_configuration_path.return_value)

    assert len(configuration.commands_repository) == 3
    for command_builder in configuration.commands_repository:
        command_builder.update_to_version.assert_called_once_with()
        assert command_builder.version is None


def test_config_init_with_fix_versions(
    cli_runner,
    mock_configuration_path,
    mock_build_configuration_from_file,
    mock_templates_provider_get_template_path,
    mock_git_repo,
    mock_cwd,
    mock_update_sources_repository,
    mock_configuration_as_dict,
):
    source_path1, source_path2, source_path3 = (
        mock_cwd / f"{SOURCE1}.py",
        mock_cwd / f"{SOURCE2}.py",
        mock_cwd / f"{SOURCE3}.py",
    )
    source_path1.touch()
    source_path2.touch()
    source_path3.touch()
    mock_build_configuration_from_file.return_value = (
        configuration
    ) = dummy_configuration()

    result = cli_runner.invoke(statue_cli, ["config", "init", "--fix-versions"])

    assert result.exit_code == 0, f"Exited with exception: {result.exception}"
    mock_configuration_path.assert_called_once_with()
    mock_git_repo.assert_called_once_with(mock_cwd)
    mock_templates_provider_get_template_path.assert_called_once_with("defaults")
    mock_build_configuration_from_file.assert_called_once_with(
        mock_templates_provider_get_template_path.return_value
    )
    mock_update_sources_repository.assert_called_once_with(
        configuration=configuration,
        sources=[
            source_path1.relative_to(mock_cwd),
            source_path2.relative_to(mock_cwd),
            source_path3.relative_to(mock_cwd),
        ],
        repo=mock_git_repo.return_value,
        exclude=(),
    )
    configuration.to_toml.assert_called_once_with(mock_configuration_path.return_value)

    assert len(configuration.commands_repository) == 3
    for command_builder in configuration.commands_repository:
        command_builder.update.assert_not_called()
        assert command_builder.installed_version is not None
        assert command_builder.version == command_builder.installed_version


@pytest.mark.parametrize(argnames="install_flag", argvalues=["-i", "--install"])
def test_config_init_with_install_and_fix_versions(
    install_flag,
    cli_runner,
    mock_configuration_path,
    mock_build_configuration_from_file,
    mock_templates_provider_get_template_path,
    mock_git_repo,
    mock_cwd,
    mock_update_sources_repository,
    mock_configuration_as_dict,
):
    source_path1, source_path2, source_path3 = (
        mock_cwd / f"{SOURCE1}.py",
        mock_cwd / f"{SOURCE2}.py",
        mock_cwd / f"{SOURCE3}.py",
    )
    source_path1.touch()
    source_path2.touch()
    source_path3.touch()
    mock_build_configuration_from_file.return_value = (
        configuration
    ) = dummy_configuration()

    result = cli_runner.invoke(
        statue_cli, ["config", "init", install_flag, "--fix-versions"]
    )

    assert result.exit_code == 0, f"Exited with exception: {result.exception}"
    mock_configuration_path.assert_called_once_with()
    mock_git_repo.assert_called_once_with(mock_cwd)
    mock_templates_provider_get_template_path.assert_called_once_with("defaults")
    mock_build_configuration_from_file.assert_called_once_with(
        mock_templates_provider_get_template_path.return_value
    )
    mock_update_sources_repository.assert_called_once_with(
        configuration=configuration,
        sources=[
            source_path1.relative_to(mock_cwd),
            source_path2.relative_to(mock_cwd),
            source_path3.relative_to(mock_cwd),
        ],
        repo=mock_git_repo.return_value,
        exclude=(),
    )
    configuration.to_toml.assert_called_once_with(mock_configuration_path.return_value)

    assert len(configuration.commands_repository) == 3
    for command_builder in configuration.commands_repository:
        command_builder.update_to_version.assert_called_once_with()
        assert command_builder.installed_version is not None
        assert command_builder.version == command_builder.installed_version


def test_config_init_without_sources(
    cli_runner,
    mock_configuration_path,
    mock_build_configuration_from_file,
    mock_templates_provider_get_template_path,
    mock_git_repo,
    mock_cwd,
    mock_update_sources_repository,
    mock_configuration_as_dict,
):
    mock_build_configuration_from_file.return_value = (
        configuration
    ) = dummy_configuration()
    result = cli_runner.invoke(statue_cli, ["config", "init", "--no-sources"])

    assert result.exit_code == 0, f"Exited with exception: {result.exception}"
    mock_configuration_path.assert_called_once_with()
    mock_git_repo.assert_not_called()
    mock_templates_provider_get_template_path.assert_called_once_with("defaults")
    mock_build_configuration_from_file.assert_called_once_with(
        mock_templates_provider_get_template_path.return_value
    )

    assert len(configuration.sources_repository) == 0

    assert len(configuration.commands_repository) == 3
    for command_builder in configuration.commands_repository:
        command_builder.update.assert_not_called()
        assert command_builder.version is None

    mock_update_sources_repository.assert_not_called()
    configuration.to_toml.assert_called_once_with(mock_configuration_path.return_value)


def test_config_init_exclude(
    cli_runner,
    mock_configuration_path,
    mock_build_configuration_from_file,
    mock_templates_provider_get_template_path,
    mock_git_repo,
    mock_cwd,
    mock_update_sources_repository,
    mock_configuration_as_dict,
):
    source_path1, source_path2, source_path3 = (
        mock_cwd / f"{SOURCE1}.py",
        mock_cwd / f"{SOURCE2}.py",
        mock_cwd / f"{SOURCE3}.py",
    )
    source_path1.touch()
    source_path2.touch()
    source_path3.touch()
    mock_build_configuration_from_file.return_value = (
        configuration
    ) = dummy_configuration()

    result = cli_runner.invoke(
        statue_cli, ["config", "init", "--exclude", str(source_path2)]
    )

    assert result.exit_code == 0, f"Exited with exception: {result.exception}"
    mock_configuration_path.assert_called_once_with()
    mock_git_repo.assert_called_once_with(mock_cwd)
    mock_templates_provider_get_template_path.assert_called_once_with("defaults")
    mock_build_configuration_from_file.assert_called_once_with(
        mock_templates_provider_get_template_path.return_value
    )
    mock_update_sources_repository.assert_called_once_with(
        configuration=configuration,
        sources=[
            source_path1.relative_to(mock_cwd),
            source_path3.relative_to(mock_cwd),
        ],
        repo=mock_git_repo.return_value,
        exclude=(source_path2,),
    )
    configuration.to_toml.assert_called_once_with(mock_configuration_path.return_value)

    assert len(configuration.commands_repository) == 3
    for command_builder in configuration.commands_repository:
        command_builder.update.assert_not_called()
        assert command_builder.version is None


def test_config_init_with_unknown_template(
    cli_runner,
    mock_configuration_path,
    mock_build_configuration_from_file,
    mock_templates_provider_get_template_path,
    mock_git_repo,
    mock_cwd,
):
    source_path1, source_path2, source_path3 = (
        mock_cwd / f"{SOURCE1}.py",
        mock_cwd / f"{SOURCE2}.py",
        mock_cwd / f"{SOURCE3}.py",
    )
    source_path1.touch()
    source_path2.touch()
    source_path3.touch()
    template_name = "template"
    mock_templates_provider_get_template_path.side_effect = UnknownTemplate(
        template_name
    )
    result = cli_runner.invoke(statue_cli, ["config", "init", "-t", template_name])

    assert result.exit_code == 3


def test_config_init_with_configuration_error(
    cli_runner,
    mock_configuration_path,
    mock_build_configuration_from_file,
    mock_templates_provider_get_template_path,
    mock_git_repo,
    mock_cwd,
):
    source_path1, source_path2, source_path3 = (
        mock_cwd / f"{SOURCE1}.py",
        mock_cwd / f"{SOURCE2}.py",
        mock_cwd / f"{SOURCE3}.py",
    )
    source_path1.touch()
    source_path2.touch()
    source_path3.touch()
    mock_build_configuration_from_file.side_effect = StatueConfigurationError(
        "This is an error message"
    )
    result = cli_runner.invoke(statue_cli, ["config", "init"])

    assert result.exit_code == 3
