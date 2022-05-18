from pathlib import Path

import mock
import pytest

from statue.exceptions import StatueTemplateError, UnknownTemplate
from statue.templates.templates_provider import TemplatesProvider
from tests.constants import SOURCE1, SOURCE2, SOURCE3, SOURCE4, SOURCE5, SOURCE6


@pytest.fixture()
def mock_templates_provider_sources(mocker):
    return mocker.patch("statue.templates.templates_provider.resources")


def test_templates_provider_user_templates_directory(mock_home):
    user_templates_directory = mock_home / ".statue" / "templates"

    assert not user_templates_directory.exists()

    assert TemplatesProvider.user_templates_directory() == user_templates_directory

    # When retrieving user templates directory, it's created
    assert user_templates_directory.exists()


def test_templates_provider_with_only_default_templates(
    mock_templates_provider_sources, mock_home
):
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
    assert TemplatesProvider.default_templates() == {toml_path1, toml_path2, toml_path3}
    assert TemplatesProvider.default_templates_names() == {SOURCE1, SOURCE2, SOURCE3}
    assert TemplatesProvider.default_templates_map() == {
        SOURCE1: toml_path1,
        SOURCE2: toml_path2,
        SOURCE3: toml_path3,
    }
    assert not TemplatesProvider.user_templates()
    assert not TemplatesProvider.user_templates_names()
    assert TemplatesProvider.user_templates_map() == {}
    assert TemplatesProvider.all_template_names() == {SOURCE1, SOURCE2, SOURCE3}
    assert TemplatesProvider.templates_map() == {
        SOURCE1: toml_path1,
        SOURCE2: toml_path2,
        SOURCE3: toml_path3,
    }
    assert TemplatesProvider.get_template_path(SOURCE1) == toml_path1
    assert TemplatesProvider.get_template_path(SOURCE2) == toml_path2
    assert TemplatesProvider.get_template_path(SOURCE3) == toml_path3


def test_templates_provider_with_only_user_templates(
    mock_templates_provider_sources, mock_home
):
    mock_templates_provider_sources.files.return_value.iterdir.return_value = []
    user_templates_directory = mock_home / ".statue" / "templates"
    user_templates_directory.mkdir(parents=True)
    toml_path1, toml_path2, toml_path3 = (
        user_templates_directory / f"{SOURCE1}.toml",
        user_templates_directory / f"{SOURCE2}.toml",
        user_templates_directory / f"{SOURCE3}.toml",
    )
    toml_path1.touch()
    toml_path2.touch()
    toml_path3.touch()

    assert TemplatesProvider.default_templates() == set()
    assert TemplatesProvider.default_templates_names() == set()
    assert TemplatesProvider.default_templates_map() == {}
    assert TemplatesProvider.user_templates() == {toml_path1, toml_path2, toml_path3}
    assert TemplatesProvider.user_templates_names() == {SOURCE1, SOURCE2, SOURCE3}
    assert TemplatesProvider.user_templates_map() == {
        SOURCE1: toml_path1,
        SOURCE2: toml_path2,
        SOURCE3: toml_path3,
    }
    assert TemplatesProvider.all_template_names() == {SOURCE1, SOURCE2, SOURCE3}
    assert TemplatesProvider.templates_map() == {
        SOURCE1: toml_path1,
        SOURCE2: toml_path2,
        SOURCE3: toml_path3,
    }
    assert TemplatesProvider.get_template_path(SOURCE1) == toml_path1
    assert TemplatesProvider.get_template_path(SOURCE2) == toml_path2
    assert TemplatesProvider.get_template_path(SOURCE3) == toml_path3


def test_templates_provider_with_both_default_and_user_templates(
    mock_templates_provider_sources, mock_home
):
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
    user_templates_directory = mock_home / ".statue" / "templates"
    user_templates_directory.mkdir(parents=True)
    toml_path4, toml_path5, toml_path6 = (
        user_templates_directory / f"{SOURCE4}.toml",
        user_templates_directory / f"{SOURCE5}.toml",
        user_templates_directory / f"{SOURCE6}.toml",
    )
    toml_path4.touch()
    toml_path5.touch()
    toml_path6.touch()

    assert TemplatesProvider.default_templates() == {toml_path1, toml_path2, toml_path3}
    assert TemplatesProvider.default_templates_names() == {SOURCE1, SOURCE2, SOURCE3}
    assert TemplatesProvider.default_templates_map() == {
        SOURCE1: toml_path1,
        SOURCE2: toml_path2,
        SOURCE3: toml_path3,
    }
    assert TemplatesProvider.user_templates() == {toml_path4, toml_path5, toml_path6}
    assert TemplatesProvider.user_templates_names() == {SOURCE4, SOURCE5, SOURCE6}
    assert TemplatesProvider.user_templates_map() == {
        SOURCE4: toml_path4,
        SOURCE5: toml_path5,
        SOURCE6: toml_path6,
    }
    assert TemplatesProvider.all_template_names() == {
        SOURCE1,
        SOURCE2,
        SOURCE3,
        SOURCE4,
        SOURCE5,
        SOURCE6,
    }
    assert TemplatesProvider.templates_map() == {
        SOURCE1: toml_path1,
        SOURCE2: toml_path2,
        SOURCE3: toml_path3,
        SOURCE4: toml_path4,
        SOURCE5: toml_path5,
        SOURCE6: toml_path6,
    }
    assert TemplatesProvider.get_template_path(SOURCE1) == toml_path1
    assert TemplatesProvider.get_template_path(SOURCE2) == toml_path2
    assert TemplatesProvider.get_template_path(SOURCE3) == toml_path3
    assert TemplatesProvider.get_template_path(SOURCE4) == toml_path4
    assert TemplatesProvider.get_template_path(SOURCE5) == toml_path5
    assert TemplatesProvider.get_template_path(SOURCE6) == toml_path6


@pytest.mark.parametrize(
    "template_name",
    [
        "template",
        "template_with_underscores",
        "TEMPLATE_IN_UPPER_CASE",
        "WeIRedTEmpLaTe",
        "template2",
        "t5mp1a7e_with_numbers",
    ],
)
def test_templates_provider_save_new_template(mock_home, template_name):
    user_templates_directory = mock_home / ".statue" / "templates"
    configuration = mock.Mock()
    TemplatesProvider.save_template(name=template_name, configuration=configuration)
    configuration.to_toml.assert_called_once_with(
        user_templates_directory / f"{template_name}.toml"
    )


def test_templates_provider_save_overrides_template(mock_home):
    user_templates_directory = mock_home / ".statue" / "templates"
    user_templates_directory.mkdir(parents=True)
    template_path = user_templates_directory / f"{SOURCE1}.toml"
    template_path.touch()
    configuration = mock.Mock()
    TemplatesProvider.save_template(
        name=SOURCE1, configuration=configuration, override=True
    )
    configuration.to_toml.assert_called_once_with(template_path)


def test_templates_provider_remove_template(mock_home):
    user_templates_directory = mock_home / ".statue" / "templates"
    user_templates_directory.mkdir(parents=True)
    template_path = user_templates_directory / f"{SOURCE1}.toml"
    template_path.touch()

    assert template_path.exists()
    TemplatesProvider.remove_template(SOURCE1)
    assert not template_path.exists()


def test_templates_provider_get_unknown_template_path(
    mock_templates_provider_sources, mock_home
):
    mock_templates_provider_sources.files.return_value.iterdir.return_value = []
    with pytest.raises(
        UnknownTemplate, match=f'^Could not find template named "{SOURCE4}"$'
    ):
        TemplatesProvider.get_template_path(SOURCE4)


def test_templates_provider_save_template_fail_due_to_existing_default_template(
    mock_templates_provider_sources, mock_home
):
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
    configuration = mock.Mock()
    with pytest.raises(
        StatueTemplateError, match=f'^"{SOURCE1}" template is already taken.$'
    ):
        TemplatesProvider.save_template(name=SOURCE1, configuration=configuration)
    configuration.to_toml.assert_not_called()


def test_templates_provider_save_template_fail_due_to_existing_user_template(mock_home):
    user_templates_directory = mock_home / ".statue" / "templates"
    user_templates_directory.mkdir(parents=True)
    template_path = user_templates_directory / f"{SOURCE1}.toml"
    template_path.touch()
    configuration = mock.Mock()
    with pytest.raises(
        StatueTemplateError, match=f'^"{SOURCE1}" template is already taken.$'
    ):
        TemplatesProvider.save_template(name=SOURCE1, configuration=configuration)
    configuration.to_toml.assert_not_called()


@pytest.mark.parametrize(
    "template_name",
    ["1template", "template@statue.com", "template.with.dots", "template with spaces"],
)
def test_templates_provider_save_template_fail_due_to_invalid_name(
    mock_home, template_name
):
    user_templates_directory = mock_home / ".statue" / "templates"
    user_templates_directory.mkdir(parents=True)
    configuration = mock.Mock()
    with pytest.raises(
        StatueTemplateError,
        match=(
            f'^"{template_name}" is an invalid template name. '
            "Templates should start with a letter and contain only "
            "letters, numbers and underscores$"
        ),
    ):
        TemplatesProvider.save_template(name=template_name, configuration=configuration)
    configuration.to_toml.assert_not_called()


def test_templates_provider_remove_template_fail_due_to_default_template(
    mock_templates_provider_sources,
):
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
        StatueTemplateError, match="^Default templates cannot be removed.$"
    ):
        TemplatesProvider.remove_template(SOURCE1)


def test_templates_provider_remove_template_fail_due_to_non_existing_template(
    mock_templates_provider_sources, mock_home
):
    mock_templates_provider_sources.files.return_value.iterdir.return_value = []
    with pytest.raises(
        UnknownTemplate, match=f'^Could not find template named "{SOURCE1}"$'
    ):
        TemplatesProvider.remove_template(SOURCE1)


def test_templates_provider_clear_user_templates(
    mock_templates_provider_sources, mock_home
):
    mock_templates_provider_sources.files.return_value.iterdir.return_value = []
    user_templates_directory = mock_home / ".statue" / "templates"
    user_templates_directory.mkdir(parents=True)
    toml_path1, toml_path2, toml_path3 = (
        user_templates_directory / f"{SOURCE1}.toml",
        user_templates_directory / f"{SOURCE2}.toml",
        user_templates_directory / f"{SOURCE3}.toml",
    )
    toml_path1.touch()
    toml_path2.touch()
    toml_path3.touch()

    assert toml_path1.exists()
    assert toml_path2.exists()
    assert toml_path3.exists()

    TemplatesProvider.clear_user_templates()

    assert not toml_path1.exists()
    assert not toml_path2.exists()
    assert not toml_path3.exists()
