# Run On Steroids
This is an advanced tutorial for the `statue run` command. For a more fundamental tutorial
please read the documentation [here](../tutorials/run_efficiently.md).

## Setting The Mode
By default, when using `statue run` all commands are running asynchronously on different sources.
That means that while *command1* is running on *sources1*, it can also run on *source2*. The same
goes for different commands.

However, two commands **does not run asynchronously on the same source**. This is done in order to
prevent different commands interfering with each other. This feature cannot be changed.

If you wish *Statue* to run only one command at a time, you can simply run:

    statue run --mode=sync

If you wish **every run** to use sync mode, you can set it in the configuration with:

    statue config set-mode sync

If you wish to turn back the default async mode, simply run:

    statue config set-mode async

## Long-Term Memory
Every time you use `statue run`, *Statue* will save the run results in history. This is done in
order to allow the user to rerun *Statue* with the same configuration.

By default, *Statue* saves the last {{ history_size() }} runs. You can change the history size
of *Statue* by running:

    statue config set-history-size new_history_size

## Incognito
By default, *Statue* will save each run of `statue run` in history. You can run *Statue* without saving to history
by running:

    statue run --no-cache

If you wish to stop *Statue* from saving results into history, you can disable caching in configuration by running:

    statue config disable-cache

If you wish to re-enable caching, simply run:

    statue config enable-cache

## Denying And Allowing Commands

We have already mentioned that a source can specify which commands to allow and which to deny.
One can allow or deny commands for the **entire run** using the `--allow` or `--deny` flags.

For example, running:

    statue run --allow command1 --allow command2

Will only run `command1` and `command2` (on sources with matching filters). On the other hand:

    statue run --deny command1 --deny command2

Will run all commands (again, according to filters), besides `command1` and `command2`.