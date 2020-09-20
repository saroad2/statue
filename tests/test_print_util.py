from unittest import mock

from pytest_cases import THIS_MODULE, parametrize_with_cases

from statue.print_util import print_title


def case_empty_title():
    title = ""
    calls = ["", ""]
    kwargs = dict()

    return title, calls, kwargs


def case_one_char_title():
    title = "a"
    calls = ["A", "="]
    kwargs = dict()

    return title, calls, kwargs


def case_one_word_title():
    title = "awesome"
    calls = ["Awesome", "======="]
    kwargs = dict()

    return title, calls, kwargs


def case_two_words_title():
    title = "awesome title"
    calls = ["Awesome Title", "============="]
    kwargs = dict()

    return title, calls, kwargs


def case_different_underline():
    title = "awesome title"
    calls = ["Awesome Title", "-------------"]
    kwargs = dict(underline="-")

    return title, calls, kwargs


@parametrize_with_cases(argnames=["title", "calls", "kwargs"], cases=THIS_MODULE)
def test_print_title(title, calls, kwargs):
    print_mock = mock.Mock()
    print_title(title, print_method=print_mock, **kwargs)
    assert print_mock.call_count == 2
    assert print_mock.call_args_list[0] == mock.call(calls[0])
    assert print_mock.call_args_list[1] == mock.call(calls[1])
