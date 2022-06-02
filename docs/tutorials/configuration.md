# Configurate It

*Statue*, like any other static code analysis tool, uses a configuration file to specify how it should operate.
This file is *statue.toml*, and it is the file that has been created when you ran `statue config init`
in the [quick start](quick_start.md) manual.

In the next few paragraphs we'll show you how to initialize the configuration file and how to edit it in order to add
new contexts and commands.

!!! note

    At the moment *Statue* does not support using *setup.cfg* and *pyproject.toml* as its configuration file.
    This feature might be considered in the future.

## What The Configuration is Made of?

*Statue*'s Configuration is made of 4 sections:

- **General Settings** - general *Statue* settings including history size and runner mode
- **Contexts Settings** - list of all available [contexts](contexts.md)
- **Commands Settings** - list of all available commands, including context specifications
- **Sources Settings** - list of all tracked sources, including which contexts to apply on them, which commands
to allow running on them and which commands to deny.

We will go through each section in a moment.

## Configuration Initialization

By now you're already familiar with the command `statue config init`. This command creates the configuration file
*statue.toml* with default contexts and commands.

When initializing the configuration file, *Statue* will add by default the contexts and commands presented in the
[default template](../templates.md).

As for sources, *Statue* will look for python scripts and packages and will ask you to approve tracking those
files. If you choose to track a source, *Statue* will ask you to specify for each source the following:

* **Contexts** - which contexts to apply when running commands on that source
* **Allowed Commands** - which commands are allowed to be run on that source. If skipped, all commands are allowed
* **Denied Commands** - which commands are denied from being run on that source. If skipped, no command is denied

!!! warning

    One can not set both "allowed commands" and "denied commands" for the same source. You can only set one of them
    or none of them.

When *Statue* ask you to track a package, you can choose to expend it in order to specify different contexts on
different modules in that package.

By default, when suggesting sources to track, *Statue* will ignore sources that are ignored by git. If you wish to
include these files in *Statue*'s search, run:

    statue config init --no-git

Moreover, if you want *Statue* to ignore tracking a specific file or a directory entirely, you can run:

    statue config init --exclude=path_to_exclude

If you wish to initialize *Statue* without any sources at all, simply run:

    statue config init --no-sources

Lastly, you can initialize empty configuration file by running:

    statue config init --blank

If you didn't run `statue config init` already, now would be the perfect time to do so before
you start editing the configuration file.


## Edit Via Command Line, Not Configuration File

One major difference between *Statue* and other static code analysis tools is that *Statue*
encourages you to never edit your configuration file manually. Instead, *Statue*'s
configuration file is fully editable via command line using the `statue config` commands.

The reason we don't recommend editing the configuration file manually is that by using
`statue config`, *Statue* can make sure that there are no conflicts in the configuration file.
If some of those conflicts emerge when you edit your configuration, *Statue* will ask you
to re-enter some fields you've filled, or it will abort.

!!! warning

    Like all other static code analysis tools, *Statue* does not save configuration file history.
    Therefore, unless you're using a VCS tool like git to track *statue.toml* changes, we
    highly recommend editing the configuration carefully.

## Editing the Configuration

It's as simple as it can get! Just run `statue config --help` and see which commands you
can use to edit the configuration file.

For example, you can run `statue config add-context` in order to add a new context to
configuration. Just follow the instruction and the new context will be added!

!!! warning

    Pay attention that using the `remove-context`, `remove-command` and `remove-source` commands will
    remove the specified context, command and source respectively, **including all of their
    references!**

## What's next?
- Learn about the [default template](../templates.md#Default Template) and which contexts and commands are
available in it
- Learn how to turn your project's configuration into a template