from unittest.mock import Mock, call

from pytest_cases import THIS_MODULE, parametrize_with_cases

from statue.print_util import print_title
from tests.util import assert_calls


def case_empty_title():
    title = ""
    calls = [call(""), call("")]
    kwargs = dict()

    return title, calls, kwargs


def case_one_char_title():
    title = "a"
    calls = [call("A"), call("=")]
    kwargs = dict()

    return title, calls, kwargs


def case_one_word_title():
    title = "awesome"
    calls = [call("Awesome"), call("=======")]
    kwargs = dict()

    return title, calls, kwargs


def case_two_words_title():
    title = "awesome title"
    calls = [call("Awesome Title"), call("=============")]
    kwargs = dict()

    return title, calls, kwargs


def case_different_underline():
    title = "awesome title"
    calls = [call("Awesome Title"), call("-------------")]
    kwargs = dict(underline="-")

    return title, calls, kwargs


def case_no_transform():
    title = "awesome title"
    calls = [call("awesome title"), call("=============")]
    kwargs = dict(transform=False)

    return title, calls, kwargs


@parametrize_with_cases(argnames=["title", "calls", "kwargs"], cases=THIS_MODULE)
def test_print_title(title, calls, kwargs):
    print_mock = Mock()
    print_title(title, print_method=print_mock, **kwargs)
    assert_calls(print_mock, calls)
