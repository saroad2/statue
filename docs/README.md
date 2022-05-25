# Welcome to *Statue*
![Python Versions](https://img.shields.io/pypi/pyversions/statue)
![PyPI Version](https://img.shields.io/pypi/v/statue)
![Maturity](https://img.shields.io/pypi/status/statue)
![License](https://img.shields.io/pypi/l/statue)
![Build Status](https://github.com/saroad2/statue/workflows/CI/badge.svg?branch=main)

Your pathway to a clean codebase.

## What's *Statue*?

*Statue* is an orchestration tool for static code analysis. It combines the overall
power of several linters and formatters into one consistent tool that prevents
unwanted conflicts. With *Statue* you can integrate tools such as *Mypy*, *Pylint*,
*Black*, *Isort* and many others.

## What Do You Mean by "Orchestration"?

When running multiple formatters and linters (commands, in general), sometimes they interfere with each other and
cause clashes. On other occasions, in order to solve an issue with one linter you have to introduce another issue
in a different linter. 

*Statue* solves this problem (and many other problems, as we'll describe later) by keeping all
your linters and formatters configuration in one file, which is fully editable via command line. In that way,
you won't need to edit huge configuration files in order to keep your commands in check.

Moreover, With *Statue* you can define different arguments for your commands to use on each file
and directory in your codebase. This allows you to customize different style conventions for different files and
directories, making your work with static code analysis tools more robust and user-friendly. This can be very handy
when you have large codebase that you want to migrate to a given style one step at a time.  

## Why *Statue*?

Statue helps you to improve your code using these powerful features:

- Run several formatters and linters asynchronously for faster evaluations
- Run commands with different arguments on each file and directory
using [contexts](contexts.md)
- Avoid editing tedious configuration files by using the `statue config` command
- Keeping results history in order to re-run failing and non-failing static code analysis tools with only few
keystrokes
- Saving your configuration as template in order for reuse in other project
- Provide clear and concise exportable evaluation reports of all your formatters and linters

## Can't I just keep all my configurations in *setup.cfg* or *pyproject.toml*?

Most of the formatters and linters allow you to save their configurations in *setup.cfg* or *pyproject.toml*.
While this solution does help keep all your configuration in one place, it doesn't allow you to specify different
configurations for different files and directories.

While *Statue* does introduce an additional configuration file (*statue.toml*), this configuration file is totally
[editable via command line](configuration.md) using the `statue config` methods.

## How does *Statue* differ from *pre-commit*?

*pre-commit* has been for a long time the go-to tool for running linters and formatters on your codebase,
and it is provided with predefined hooks for most state-of-the-art tools.
While we surely recommend on using *pre-commit*, here are few reasons why you might want to consider also
using *Statue*:

* If you don't need each and every commit to pass your linters
* If you want to use a linters and formatters that doesn't have *.pre-commit-hooks.yaml* file
* If you use a lot of linters and formatters which cause your `git commit` to hang for long periods of time
* If you want to run your linters and formatters with different arguments on different files and directories
* If you need clear and concise reports of your linters evaluations


## What's next?

- Go on to the [quick start](quick_start.md) tutorial in order to begin using *Statue* in a few 
short steps
- Learn [a few tips](run_efficiently.md) how to use `statue run` efficiently