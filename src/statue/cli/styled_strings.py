"""Transforming plane strings into styled ones."""
import click


def source_style(source: str) -> str:
    """
    Styling function to emphasise sources paths.

    :param source: The source name to style
    :type source: str
    :return: Styles source
    :rtype: str
    """
    return click.style(source, fg="cyan")


def name_style(name: str) -> str:
    """
    Styling function to emphasise names.

    :param name: The name to style
    :type name: str
    :return: Styled name
    :rtype: str
    """
    return click.style(name, fg="magenta")


def bullet_style(bullet_name: str) -> str:
    """
    Styling function to emphasise bullet names.

    :param bullet_name: The name to style
    :type bullet_name: str
    :return: Styled bullet name
    :rtype: str
    """
    return click.style(bullet_name, fg="yellow")


def success_style(success_string: str) -> str:
    """
    Styling function to emphasise bullet names.

    :param success_string: The string to style
    :type success_string: str
    :return: Styled success string
    :rtype: str
    """
    return click.style(success_string, fg="green")


def failure_style(failure_string: str) -> str:
    """
    Styling function to emphasise bullet names.

    :param failure_string: The string to style
    :type failure_string: str
    :return: Styled failure string
    :rtype: str
    """
    return click.style(failure_string, fg="red")
