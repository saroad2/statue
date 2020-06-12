import pytest


@pytest.fixture
def existing_settings(tmp_path):
    return tmp_path


@pytest.fixture
def non_existing_settings(tmpdir):
    return tmpdir / "non_existing_settings.toml"


@pytest.fixture
def existing_input1(tmp_path):
    return tmp_path


@pytest.fixture
def existing_input2(tmp_path):
    return tmp_path


@pytest.fixture
def existing_input3(tmp_path):
    return tmp_path


@pytest.fixture
def non_existing_input_file1(tmpdir):
    return tmpdir / "non_existing_input1.py"


@pytest.fixture
def non_existing_input_file2(tmpdir):
    return tmpdir / "non_existing_input2.py"
