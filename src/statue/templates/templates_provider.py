"""Configuration templates provider."""
import re
import sys
from pathlib import Path
from typing import Dict, Set, Union

from statue.config.configuration import Configuration
from statue.constants import TEMPLATE_NAME_REGEX
from statue.exceptions import StatueTemplateError, UnknownTemplate

if sys.version_info < (3, 9):  # pragma: no cover
    import importlib_resources as resources
    from importlib_resources.abc import Traversable
else:  # pragma: no cover
    from importlib import resources
    from importlib.abc import Traversable


TemplateSourceType = Union[Traversable, Path]


class TemplatesProvider:
    """A singleton for retrieving configuration templates."""

    @classmethod
    def default_templates_map(cls) -> Dict[str, Traversable]:
        """
        Creates map from default template name to path.

        :return: templates map.
        :rtype: Dict[str, Traversable]
        """
        return {
            cls.get_template_name(path): path
            for path in TemplatesProvider.default_templates()
        }

    @classmethod
    def user_templates_map(cls) -> Dict[str, Path]:
        """
        Creates map from user template name to path.

        :return: templates map.
        :rtype: Dict[str, Path]
        """
        return {
            cls.get_template_name(path): path
            for path in TemplatesProvider.user_templates()
        }

    @classmethod
    def templates_map(cls) -> Dict[str, TemplateSourceType]:
        """
        Creates map from template name to path.

        :return: templates map.
        :rtype: Dict[str, Traversable]
        """
        return {**cls.default_templates_map(), **cls.user_templates_map()}

    @classmethod
    def default_templates(cls) -> Set[Traversable]:
        """
        Get all default templates available.

        :return: default templates
        :rtype: Set[Traversable]
        """
        return {
            path
            for path in resources.files("statue.templates.default_templates").iterdir()
            if path.name.split(".")[-1] == "toml"
        }

    @classmethod
    def user_templates(cls) -> Set[Path]:
        """
        Get all user templates available.

        :return: User templates
        :rtype: Set[Path]
        """
        return set(cls.user_templates_directory().iterdir())

    @classmethod
    def default_templates_names(cls) -> Set[str]:
        """
        Get all default template names.

        :return: all default template names
        :rtype: Set[str]
        """
        return {cls.get_template_name(path) for path in cls.default_templates()}

    @classmethod
    def user_templates_names(cls) -> Set[str]:
        """
        Get all user template names.

        :return: all user template names
        :rtype: Set[str]
        """
        return {cls.get_template_name(path) for path in cls.user_templates()}

    @classmethod
    def all_template_names(cls) -> Set[str]:
        """
        Get all available template names.

        :return: all template names
        :rtype: Set[str]
        """
        return {*cls.default_templates_names(), *cls.user_templates_names()}

    @classmethod
    def get_template_path(cls, template_name: str) -> Traversable:
        """
        Get a template path by name.

        :param template_name: name of the template path to retrieve
        :type template_name: str
        :return: requested template path
        :rtype: Traversable
        :raises UnknownTemplate: raised when given template name is unknown
        """
        try:
            return cls.templates_map()[template_name]
        except KeyError as error:
            raise UnknownTemplate(template_name) from error

    @classmethod
    def user_templates_directory(cls) -> Path:
        """
        Get user templates directory.

        :return: User templates directory
        :rtype: Path
        """
        templates_directory = Path.home() / ".statue" / "templates"
        templates_directory.mkdir(parents=True, exist_ok=True)
        return templates_directory

    @classmethod
    def get_template_name(cls, path: TemplateSourceType) -> str:
        """
        Get template name from path.

        :param path: Path of the template
        :type path: TemplateSourceType
        :return: Template name
        :rtype: str
        """
        return path.name.split(".")[0]

    @classmethod
    def save_template(
        cls, name: str, configuration: Configuration, override: bool = False
    ):
        """
        Save configuration as template with given name.

        :param name: Name of the template to save
        :type name: str
        :param configuration: Configuration to be saved as template
        :type configuration: Configuration
        :param override: Should override existing template. False by default.
        :type override: bool
        :raises StatueTemplateError: raised when configuration cannot be
            saved as a template.
        """
        if not re.match(TEMPLATE_NAME_REGEX, name):
            raise StatueTemplateError(
                f'"{name}" is an invalid template name. '
                "Templates should start with a letter and contain only "
                "letters, numbers and underscores"
            )
        if not override and name in cls.all_template_names():
            raise StatueTemplateError(f'"{name}" template is already taken.')
        configuration.to_toml(cls.user_templates_directory() / f"{name}.toml")

    @classmethod
    def remove_template(cls, name: str):
        """
        Remove user defined template.

        :param name: Name of the template to be removed
        :type name: str
        :raises StatueTemplateError: Raised when trying to remove a default template
        :raises UnknownTemplate: Raised when there is no template with given name
        """
        if name in cls.default_templates_names():
            raise StatueTemplateError("Default templates cannot be removed.")
        try:
            template_path = cls.user_templates_map()[name]
            template_path.unlink()
        except KeyError as error:
            raise UnknownTemplate(name) from error

    @classmethod
    def clear_user_templates(cls):
        """Remove all user templates."""
        for template_path in cls.user_templates():
            template_path.unlink()
