from unittest import mock

from pytest_cases import THIS_MODULE, parametrize_with_cases

from statue.cli.cli import statue_cli
from statue.constants import CONTEXTS, SOURCES, STANDARD


def mock_path(posix_path, is_dir=False):
    path = mock.MagicMock()
    path.as_posix.return_value = posix_path
    path.is_dir.return_value = is_dir
    return path


def case_empty_sources():
    return [], [], {SOURCES: {}}


def case_one_source_with_default_yes():
    src_path = "src"
    src = mock_path(src_path)
    return [src], ["", ""], {SOURCES: {src_path: {CONTEXTS: [STANDARD]}}}


def case_one_source_with_yes():
    src_path = "src"
    src = mock_path(src_path)
    return [src], ["y", ""], {SOURCES: {src_path: {CONTEXTS: [STANDARD]}}}


def case_one_source_with_no():
    src = mock_path("src")
    return [src], ["n"], {SOURCES: {}}


def case_one_source_with_yes_and_one_context_override():
    src_path = "src"
    src = mock_path(src_path)
    return [src], ["y", "foo"], {SOURCES: {src_path: {CONTEXTS: ["foo"]}}}


def case_one_source_with_yes_and_multiple_contexts_override():
    src_path = "src"
    src = mock_path(src_path)
    return [src], ["y", "foo, bar"], {SOURCES: {src_path: {CONTEXTS: ["foo", "bar"]}}}


def case_expend_with_all_yes(mock_expend, mock_git_repo):
    src_path = "src"
    src = mock_path(src_path, is_dir=True)
    one, two, three = "src/one", "src/two", "src/three"
    mock_expend.return_value = [mock_path(path) for path in [one, two, three]]
    yield [src], ["e", "y", "", "y", "", "y", ""], {
        SOURCES: {
            one: {CONTEXTS: [STANDARD]},
            two: {CONTEXTS: [STANDARD]},
            three: {CONTEXTS: [STANDARD]},
        }
    }
    mock_expend.assert_called_once_with(src, repo=mock_git_repo.return_value)


def case_expend_with_one_no(mock_expend, mock_git_repo):
    src_path = "src"
    src = mock_path(src_path, is_dir=True)
    one, two, three = "src/one", "src/two", "src/three"
    mock_expend.return_value = [mock_path(path) for path in [one, two, three]]
    yield [src], ["e", "y", "", "n", "y", ""], {
        SOURCES: {one: {CONTEXTS: [STANDARD]}, three: {CONTEXTS: [STANDARD]}}
    }
    mock_expend.assert_called_once_with(src, repo=mock_git_repo.return_value)


def case_expended_get_contexts(mock_expend, mock_git_repo):
    src_path = "src"
    test_path = "test"
    src = mock_path(src_path, is_dir=True)
    test = mock_path(test_path, is_dir=True)
    one, two, three = "test/one", "test/two", "test/three"
    mock_expend.return_value = [mock_path(path) for path in [one, two, three]]
    yield [src, test], ["y", "", "e", "y", "fast", "y", "", "y", "format"], {
        SOURCES: {
            src_path: {CONTEXTS: [STANDARD]},
            one: {CONTEXTS: ["fast"]},
            two: {CONTEXTS: ["test"]},
            three: {CONTEXTS: ["format"]},
        }
    }
    mock_expend.assert_called_once_with(test, repo=mock_git_repo.return_value)


@parametrize_with_cases(
    argnames=["sources", "inputs", "expected_config"], cases=THIS_MODULE
)
def test_interactive_config_init(
    sources,
    inputs,
    expected_config,
    mock_load_configuration,
    mock_configuration_path,
    mock_cwd,
    mock_find_sources,
    mock_toml_dump,
    mock_git_repo,
    cli_runner,
):
    mock_sources = []
    for source in sources:
        mock_source = mock.Mock()
        mock_source.relative_to.return_value = source
        mock_sources.append(mock_source)
    mock_find_sources.return_value = mock_sources
    mock_open = mock.mock_open()
    with mock.patch("statue.cli.config.open", mock_open):
        result = cli_runner.invoke(
            statue_cli, ["config", "init", "-i"], input="\n".join(inputs)
        )
    assert result.exit_code == 0, f"Exit with code different than 0. {result.exception}"
    mock_open.assert_called_once_with(mock_configuration_path.return_value, mode="w")
    mock_toml_dump.assert_called_once_with(expected_config, mock_open.return_value)
    mock_find_sources.assert_called_once_with(mock_cwd, repo=mock_git_repo.return_value)
