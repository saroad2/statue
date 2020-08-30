Statue
=========

.. image:: https://img.shields.io/pypi/pyversions/statue.svg
   :target: https://pypi.python.org/pypi/statue
   :alt: Python Versions

.. image:: https://img.shields.io/pypi/v/statue.svg
   :target: https://pypi.python.org/pypi/statue
   :alt: PyPI Version

.. image:: https://img.shields.io/pypi/status/statue.svg
   :target: https://pypi.python.org/pypi/statue
   :alt: Maturity

.. image:: https://img.shields.io/pypi/l/statue.svg
   :target: https://github.com/saroad2/statue/blob/master/LICENSE
   :alt: License

.. image:: https://github.com/saroad2/statue/workflows/CI/badge.svg?branch=master
   :target: https://github.com/saroad2/statue/actions
   :alt: Build Status

.. image:: https://codecov.io/gh/saroad2/statue/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/saroad2/statue
  :alt: CodeCov


*Statue* is an orchestration tool for static code analysis. It combines the overall
power of several linters and formatters into one consistent tool that prevents
unwanted conflicts. With *Statue* you can integrate tools such as *mypy*, *pylint*,
*black*, *isort* and many others.

Installation
------------

In order to install *Statue*, run:

::

    pip install statue

Simple Usage
------------

In order to run *Statue* over a source folder ``src`` with standard context, run:

::

    statue run src

Run In Context
--------------

Run *Statue* in specific contexts in order to evaluate different files in various ways.
For example, run *Statue* over a unit tests folder with the "test" context:

::

    statue run unit_tests --context=test

Use A Configuration File
------------------------

Add a configuration file in order let statue know how to evaluate your code.
simply add a **statue.toml** file to your repository's root directory. Here's an example
file:

.. code:: toml

    [sources.src]

    [sources.tests]
    contexts = ["test"]

Now you can simply run ``statue run`` and *Statue* will evaluate you repository without
contexts problems.

Contributing
------------

If you experience problems with Statue, `log them on GitHub`_.

If you want to contribute code, please `fork the code`_ and `submit a pull request`_.

.. _log them on Github: https://github.com/saroad2/statue/issues
.. _fork the code: https://github.com/saroad2/statue
.. _submit a pull request: https://github.com/saroad2/statue/pulls
