import os

import pytest

from statue.command import Command

ENVIRON = dict(s=2, d=5, g=8)


@pytest.fixture
def environ(monkeypatch):
    monkeypatch.setattr(os, "environ", ENVIRON)
    return ENVIRON


@pytest.fixture
def mock_subprocess(mocker):
    return mocker.patch("subprocess.run")


@pytest.fixture
def mock_get_package(mocker):
    return mocker.patch.object(Command, "_get_package")
