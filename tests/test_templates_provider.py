from pathlib import Path

import pytest

from statue.exceptions import UnknownTemplate
from statue.templates.templates_provider import TemplatesProvider
from tests.constants import SOURCE1, SOURCE2, SOURCE3, SOURCE4


@pytest.fixture()
def mock_templates_provider_sources(mocker):
    return mocker.patch("statue.templates.templates_provider.resources")


def test_templates_provider_default_templates(mock_templates_provider_sources):
    toml_path1, toml_path2, toml_path3 = (
        Path(f"{SOURCE1}.toml"),
        Path(f"{SOURCE2}.toml"),
        Path(f"{SOURCE3}.toml"),
    )
    dummy_path1, dummy_path2 = Path("dummy1"), Path("dum2my")
    mock_templates_provider_sources.files.return_value.iterdir.return_value = [
        toml_path1,
        dummy_path1,
        toml_path2,
        toml_path3,
        dummy_path2,
    ]
    assert TemplatesProvider.default_templates() == [toml_path1, toml_path2, toml_path3]


def test_templates_provider_templates_map(mock_templates_provider_sources):
    toml_path1, toml_path2, toml_path3 = (
        Path(f"{SOURCE1}.toml"),
        Path(f"{SOURCE2}.toml"),
        Path(f"{SOURCE3}.toml"),
    )
    dummy_path1, dummy_path2 = Path("dummy1"), Path("dum2my")
    mock_templates_provider_sources.files.return_value.iterdir.return_value = [
        toml_path1,
        dummy_path1,
        toml_path2,
        toml_path3,
        dummy_path2,
    ]
    assert TemplatesProvider.templates_map() == {
        SOURCE1: toml_path1,
        SOURCE2: toml_path2,
        SOURCE3: toml_path3,
    }


def test_templates_provider_template_names(mock_templates_provider_sources):
    toml_path1, toml_path2, toml_path3 = (
        Path(f"{SOURCE1}.toml"),
        Path(f"{SOURCE2}.toml"),
        Path(f"{SOURCE3}.toml"),
    )
    dummy_path1, dummy_path2 = Path("dummy1"), Path("dum2my")
    mock_templates_provider_sources.files.return_value.iterdir.return_value = [
        toml_path1,
        dummy_path1,
        toml_path2,
        toml_path3,
        dummy_path2,
    ]
    assert TemplatesProvider.template_names() == [SOURCE1, SOURCE2, SOURCE3]


def test_templates_provider_get_template_path(mock_templates_provider_sources):
    toml_path1, toml_path2, toml_path3 = (
        Path(f"{SOURCE1}.toml"),
        Path(f"{SOURCE2}.toml"),
        Path(f"{SOURCE3}.toml"),
    )
    dummy_path1, dummy_path2 = Path("dummy1"), Path("dum2my")
    mock_templates_provider_sources.files.return_value.iterdir.return_value = [
        toml_path1,
        dummy_path1,
        toml_path2,
        toml_path3,
        dummy_path2,
    ]
    assert TemplatesProvider.get_template_path(SOURCE1) == toml_path1
    assert TemplatesProvider.get_template_path(SOURCE2) == toml_path2
    assert TemplatesProvider.get_template_path(SOURCE3) == toml_path3


def test_templates_provider_get_unknown_template_path(mock_templates_provider_sources):
    toml_path1, toml_path2, toml_path3 = (
        Path(f"{SOURCE1}.toml"),
        Path(f"{SOURCE2}.toml"),
        Path(f"{SOURCE3}.toml"),
    )
    dummy_path1, dummy_path2 = Path("dummy1"), Path("dum2my")
    mock_templates_provider_sources.files.return_value.iterdir.return_value = [
        toml_path1,
        dummy_path1,
        toml_path2,
        toml_path3,
        dummy_path2,
    ]
    with pytest.raises(
        UnknownTemplate, match=f'^Could not find template named "{SOURCE4}"$'
    ):
        TemplatesProvider.get_template_path(SOURCE4)
