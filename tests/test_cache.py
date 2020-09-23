from pytest_cases import fixture, fixture_ref, parametrize

from statue.cache import Cache


@fixture()
def mock_cache_dir(mock_cwd):
    cache_dir = mock_cwd.__truediv__.return_value
    yield cache_dir
    mock_cwd.__truediv__.assert_called_once_with(".statue")


@fixture()
def mock_existing_cache_dir(mock_cache_dir):
    mock_cache_dir.exists.return_value = True
    yield mock_cache_dir
    mock_cache_dir.mkdir.assert_not_called()


@fixture()
def mock_non_existing_cache_dir(mock_cache_dir):
    mock_cache_dir.exists.return_value = False
    yield mock_cache_dir
    mock_cache_dir.mkdir.assert_called_once_with()


@parametrize(
    argnames="cache_dir",
    argvalues=[
        fixture_ref(mock_existing_cache_dir),
        fixture_ref(mock_non_existing_cache_dir),
    ],
)
def test_cache_dir(cache_dir):
    actual_statue_dir = Cache.cache_dir()
    assert actual_statue_dir == cache_dir


@parametrize(
    argnames="cache_dir",
    argvalues=[
        fixture_ref(mock_existing_cache_dir),
        fixture_ref(mock_non_existing_cache_dir),
    ],
)
def test_cache_file(cache_dir):
    file_name = "file.txt"
    actual_cache_file = Cache.cache_file(file_name)
    assert actual_cache_file == cache_dir.__truediv__.return_value
    cache_dir.__truediv__.assert_called_once_with(file_name)


@parametrize(
    argnames="cache_dir",
    argvalues=[
        fixture_ref(mock_existing_cache_dir),
        fixture_ref(mock_non_existing_cache_dir),
    ],
)
def test_cache_last_evaluation(cache_dir):
    actual_cache_file = Cache.last_evaluation_path()
    assert actual_cache_file == cache_dir.__truediv__.return_value
    cache_dir.__truediv__.assert_called_once_with("evaluation.json")
