from unittest.mock import Mock, call

from pytest_cases import THIS_MODULE, parametrize_with_cases

from statue.print_util import print_boxed
from tests.util import assert_calls


def case_empty_text():
    title = ""
    calls = [call("####"), call("#  #"), call("####")]
    kwargs = {}

    return title, calls, kwargs


def case_one_char_text():
    title = "a"
    calls = [call("#####"), call("# A #"), call("#####")]
    kwargs = {}

    return title, calls, kwargs


def case_one_word_text():
    title = "awesome"
    calls = [call("###########"), call("# Awesome #"), call("###########")]
    kwargs = {}

    return title, calls, kwargs


def case_two_words_text():
    title = "awesome title"
    calls = [
        call("#################"),
        call("# Awesome Title #"),
        call("#################"),
    ]
    kwargs = {}

    return title, calls, kwargs


def case_different_border():
    title = "awesome title"
    calls = [
        call("$$$$$$$$$$$$$$$$$"),
        call("$ Awesome Title $"),
        call("$$$$$$$$$$$$$$$$$"),
    ]
    kwargs = dict(border="$")

    return title, calls, kwargs


@parametrize_with_cases(argnames=["title", "calls", "kwargs"], cases=THIS_MODULE)
def test_print_boxed(title, calls, kwargs):
    print_mock = Mock()
    print_boxed(title, print_method=print_mock, **kwargs)
    assert_calls(print_mock, calls)
