# User Templates

We've already discussed how to initialize the configuration from the
[default template](../templates.md#Default Template) and how to create blank configuration file.
However, you often want to create a template of your own in order to reuse it in multiple projects.
This can be easily done with *Statue*.

## Thinking Globally

After editing a configuration file for a specific project by adding and removing commands and context,
you can save this configuration as a template by running:

    statue templates save new_template_name

This will save all the contexts and commands, including contexts specifications, as a template with
the given name.

!!! note

    Template names must start with letters and contain only letters, numbers and underscores.
    You cannot use the same template name twice and cannot use 

## Using New Templates

After saving your configuration as template, you can start using it in other projects.
You can see all the available templates by running:

    statue templates list

You can see which contexts and commands are available for each template by running:

    statue templates show tempalte_name

In order to create a new configuration file in another project, you can simply run:

    statue config init --template=template_name

and the configuration file will be created according to that template.

!!! note

    While templates contain commands and contexts, they do not contain sources specifications.
    That means that when using a template for a new project, make sure to respecify contexts and
    commands for the sources of that project.

## Keeping Things Up-To-Date

When you create a template from a project configuration, changing the configuration file
will not affect the template. If you wish to update the template according to the project configuration
run:

    statue templates save template_name --override

## Removing Templates

You can remove a user template by running:

    statue templates remove template_name

If you wish to remove all user templates, simply run:

    statue templates clear

!!! note

    Default templates cannot be removed by the user

!!! warning

    When a template is removed via the `remove` and `clear` command, it cannot be restored.
