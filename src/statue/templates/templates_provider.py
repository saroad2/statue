"""Configuration templates provider."""
import sys
from typing import Dict, List

from statue.exceptions import UnknownTemplate

if sys.version_info < (3, 9):  # pragma: no cover
    import importlib_resources as resources
    from importlib_resources.abc import Traversable
else:  # pragma: no cover
    from importlib import resources
    from importlib.abc import Traversable


class TemplatesProvider:
    """A singleton for retrieving configuration templates."""

    @classmethod
    def templates_map(cls) -> Dict[str, Traversable]:
        """
        Creates map from template name to path.

        :return: templates map.
        :rtype: Dict[str, Traversable]
        """
        return {
            path.name.split(".")[0]: path
            for path in TemplatesProvider.default_templates()
        }

    @classmethod
    def default_templates(cls) -> List[Traversable]:
        """
        Get all default templates available.

        :return: default templates
        :rtype: List[Traversable]
        """
        return [
            path
            for path in resources.files("statue.templates.default_templates").iterdir()
            if path.name.split(".")[-1] == "toml"
        ]

    @classmethod
    def template_names(cls) -> List[str]:
        """
        Get all available template names.

        :return: all available template names
        :rtype: List[str]
        """
        return list(cls.templates_map().keys())

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
