# Taking Contexts to The Next Level
We've already discussed [contexts](../tutorials/contexts.md) and how to use them. Now
it's time to take things for the next level. Here are some advanced abilities you can use
to unleash the full power of contexts.

## Attaching A Context to A Source
You added a new context and used an existing context and ran *Statue* with that context:

    statue run -c your_context

But two things bother you:

1. You don't want to use that context on all of your codebase
2. You want to attach this context to a specific source on **every run**

Fortunately, *Statue* can attach a context to a specific source and use that context every time
a command is running on that context. You attach a context to a source in three ways:

1. When you initialize *Statue* and run `statue config init`, when your source is presented, choose
tracking it and choose your context to attach
2. If you already initialized *Statue* and the source is not tracked, you can track the source by running
`statue config add-source your_source` and when asked to specify contexts, specify the desired context
3. If you already initialized *Statue* and the source is tracked, do the same as 2. but run
`statue config edit-source your_source`.

## A Friendly Context
By default, when presenting a context, a command will not run unless it comply one of the following:

* The context is allowed for this command
* The context is required for that command
* The context is specified for that command

Each of the three possibilities requires the **command** to declare what to do with the **context**.
However, sometimes you want the context to be allowed by default for all commands, meaning that
by default, if the context is present the command will run the same as it would without it.

In order to do exactly that you can define a context as *allowed by default* in the configuration.
Just edit the context using `statue config edit-context your_context` and set *allowed by default*
to true. If the context is non-existing, when adding it using `statue config add-context` specify
it as allowed by default.

!!! note

    If a context is explicitly denied for a command using the *denied contexts* field, the command
    will not run when the context is presented, even if it is allowed by default

## Keeping Things In The Family
A powerful tool that contexts present is *parenting*, meaning that one context can be a parent of
another context.

How is that helpful? let's assume we have a context *child* which has a parent context *parent*.
Now, if we run `statue run -c child`, the followings can happen when choosing how to run a command:

* If *child* is defined for the command (allowed, required, denied or specified) than
that behaviour will take place.
* Otherwise, if *parent* is defined for the command than that behaviour will take place
* If both are not defined than the command will run if and only if *child* is allowed by default

The usage of children contexts is very helpful for deeper specifications for commands. If we
introduce a child context of another context it allows us to defined even more specific behavior
for certain commands.

Pay attention that one can create a chain of parents (grandparent, great-grandparent,
great-great-grandparent, etc.) such that the behavior of the command will be taken from
the closest ancestor to the given context which is explicitly defined for the command.

!!! note

    While each context can have multiple children, contexts can have at most one parent

You can define parents when editing a context (`statue config edit-context`) or adding one
(`statue config add-context`).

## Living Under An Alias
Naming things can be tricky. On the one hand, you want a meaningful name, even if it's a long
one. On the other hand, you don't want to write long names every time. The same goes for contexts.

Using an *alias* allows you to name your context with a meaningful name, but allowing users to
call that context with a shorter name.

For example, in our [default template](../templates.md#default-template) we have the
**documentation** context. This is a long name! However, this context has an alias: *docs*.
That means that instead of running:

    statue run -c documentation

You can run:

    statue run -c docs

You can use a context's alias instead of its name **everywhere**, including when specifying
a context in the configuration. *Statue* will make sure to translate the alias to the real name of
the context.

!!! note

    A context can have more than one alias. The aliases can be used intechangably.

## Keeping Things In Order
Contexts are a strong tool as they are, combining multiple contexts is even more powerful!
If you run:

    statue run -c context1 -c context2 ...

*Statue* will run will process all the commands with the presented contexts.
Contexts that are allowed or required by a command will not change the arguments of this command.
However, contexts that are specified for a command will change the arguments
**according to the order that they are presented in the command line**.

Here's an example: assume that *context1* adds the arguments "a", "b" and "c" to the command
*my_command* and *context2* clears the arguments entirely for that command.
By default, *my_command* runs with the arguments "r", "t" and "s". When running:

    statue run -c context1 -c context2

*my_command* will run without any arguments, since it first added "a", "b" and "c", and then
cleared all the arguments, including the ones added by *context1*:

    my_command arguments = [r t s] => (context1) => [r t s a b c] => (context2) => []

However, if you run:

    statue run -c context2 -c context1

*my_command* will run with the arguments "a", "b" and "c", since it first cleared all arguments
(and removed "r", "t" and "s") and then added "a", "b" and "c":

    my_command arguments = [r t s] => (context2) => [] => (context1) => [a b c]

On the contrary, if both of your context simply add arguments, and the command is invariant
to the order to arguments, than changing the order to contexts will not affect the end result
of the command run.

Pay attention that the same is true when specifying contexts in the sources configuration!
The order of contexts defined for the source is the order that the contexts will be processed.

!!! note

    contexts which are attached to a given source will be processed after gloval contexts.
    That means that when running `statue run -c context1` of a source with attached context
    *context2*, *context1* will be processed before *context2*.