from pytest_cases import fixture

from statue.configuration import Configuration


@fixture
def mock_find_sources(mocker):
    return mocker.patch("statue.cli.config.find_sources")


@fixture
def mock_expend(mocker):
    return mocker.patch("statue.cli.config.expend")


@fixture
def mock_configuration_path(mocker):
    return mocker.patch.object(Configuration, "configuration_path")


@fixture
def mock_git_repo(mocker):
    return mocker.patch("git.Repo")
