from pytest_cases import fixture


@fixture
def mock_find_sources(mocker):
    return mocker.patch("statue.cli.config.find_sources")


@fixture
def mock_expend(mocker):
    return mocker.patch("statue.cli.config.expend")


@fixture
def mock_git_repo(mocker):
    return mocker.patch("git.Repo")
