# It's All A Matter of Context

## What's Context?

Contexts are the way of *Statue* to declare that a command (or multiple commands) should be running with different
arguments than the default ones. By presenting a context you can inform *Statue* what kind of checks you want your
linters to run or avoid running, and how to address each source in your codebase.

## The Power Of Contexts

The use of contexts presents few major advantages:

* Using the same context name for multiple commands allows you to change the arguments of huge number
of commands with a single magic word
* [Attaching](../advanced/advanced_contexts.md#attaching-a-context-to-a-source) a context to a
source helps you to direct the commands how to run on that particular source.
* Turning commands on and off when introducing a context which they don't comply with.
* [Joining](../advanced/advanced_contexts.md#keeping-things-in-order) few contexts together allows
you to express complex specifications for a given command or source
* [Parenting](../advanced/advanced_contexts.md#keeping-things-in-the-family) context makes it easy
to demonstrate increasingly specific requirements for a given command or source
* [Aliasing](../advanced/advanced_contexts.md#living-under-an-alias) a context for more fluent
usage of that context

Using contexts wisely when running *Statue* can help you to reduce time spent on code reviews and broken CI processes.
Just run *Statue* with the right contexts, and *Statue* will take it from there.

On the next few paragraph, we'll show you how to do exactly that.

## Presenting A Context on Specific Run

If you want to run *Statue* with a context, simply run:

    statue run -c your_context_name

if you want to see which contexts are available, run:

    statue context list

## It's A Game Changer!

If you want to see how a context affect your commands, simply run:

    statue contexts show your_context_name

After that, you'll see that the context can affect commands in four ways:

* *Required by*: If a context is required by a command, it means that the command will
not run at all unless the context is presented
* *Allowed by*: If a context is allowed by a commands, it means that the command will
run the same way when this context is presented without changing its arguments
* *Denied by*: If a context is denied by a command, it means that the command will not
run if the context is present. This includes commands which are allowed by default
* *Specified for*: If a context is specified for a command, it means that presenting this
context will change the arguments of the command.

If you want to see exactly how a specified context change the arguments of a command,
simply run:

    statue commands show your_command_name

As you'll see, a context can change a command in 3 ways:

* *Override arguments*: Override all existing arguments and replace them with new ones
* *Add arguments*: Keep all existing arguments, but add new ones at the end of the command
* *Clear arguments* Remove all arguments of the command

Different contexts can change a command in different ways. Be sure to use the right context
in the right situation to elevate your code writing routines.

## Special Treatment

One of the most common uses one might use contexts for is to inform commands to run
differently on sources. This is done by editing *Statue*'s configuration file.

## Example 1: The "Format" Context

If you're using *Statue*'s default template than by default all the formatters are in "check"
mode. That means that they will not change your source code when using `statue run`, but return
an error code if your code does not match their format.

If you want the formatters to format your code, you must use the "format" context.
You can do it by running:

    statue run -c format

## Example 2: The "Test" Context

Most linters use the same heuristics to check all of your codebase, while normally allowing you
to ignore specific regular expressions or entire files and directories.
However, you might want to keep running the linters on all of your codebase, just with different checks
on different sources.

A good example for that is unit tests. *Pylint* requires by default that every function will be given a
docstring. However, most developers agree that unit test functions don't have to include docstrings since their titles
should be meaningful enough. This is where the "test" context come in handly.

By adding the "test" context to your unit tests' directory, *Statue* will remove checks that
are not required for unit tests. You can do it by editing the configuration file.

## What's next?
- Learn how to edit the [configuration](configuration.md) file via the command line
- Learn about the [default template](../templates.md#Default Template) and which contexts and commands are
available in it
- Learn about more [advanced abilities](../advanced/advanced_contexts.md) of contexts