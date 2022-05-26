# Quick Start

## Installation
In order to install *Statue*, simply run:

    pip install statue

You can validate statue has been installed successfully by running:

    statue --version

Which will print:

    statue, version {{ version()  }}

## Initialize *Statue*

In order for *Statue* to work correctly, you need to initialize *Statue*'s configuration file.
This is simply done by going to your project's root directory and using the command:

    statue config init

This command will create *statue.toml* file with the relevant configurations. Just follow the instructions, and your
*Statue* configuration file will be ready!

You can see which commands have been set in your configuration using the command:

    statue config show-tree

If you want to look at your configuration file as plain text, you can alternatively use:

    statue config show

!!! note

    When using `statue config init`, *Statue* will ask you to specify for each source which [contexts](contexts.md),
    allowed commands and denied commands to apply to that source. If you are not sure how to respond, skip by pressing
    enter. You'll always be able to edit your configuration later.

## Run!
Now that your configuration file is ready, simply run:

    statue run
   
And all the commands defined in the configuration will run on your codebase.

!!! note

    When running `statue run`, *Statue* creates a cache directory named *.statue* which is saved in your project's
    root directory. If you're using *git* as your VCS tool we highly recommend that you add *.statue* to your
    *.gitignore* file. 

## What's Next?
- Learn how to use `statue run` in various ways to [improve efficiency](run_efficiently.md)
- Learn how to use [contexts](contexts.md) in order to specify the way you want your formatters
and linters to run
- Learn how to edit your [configuration](configuration.md) file via command line