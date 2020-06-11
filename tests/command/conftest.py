import pytest
import os


ENVIRON = dict(s=2, d=5, g=8)


@pytest.fixture
def subprocess_mock(mocker):
    return mocker.patch("subprocess.run")


@pytest.fixture
def environ(monkeypatch):
    monkeypatch.setattr(os, "environ", ENVIRON)
    return ENVIRON


@pytest.fixture
def print_mock(mocker):
    return mocker.patch("builtins.print")
