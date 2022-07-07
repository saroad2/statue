# Integrations

Playing together is always better than playing alone. Therefore, we believe that *Statue*
should play well with others. Here are a few tools that can be integrated with *Statue*. We are working
towards enabling as many as integrations as possible for a collaborative ecosystem of open-source tools.

## Pre-Commit
You can use *Statue* as a [pre-commit](https://github.com/pre-commit/pre-commit) hook in order to run statue on
every commit. You can do so by adding the following section to your *.pre-commit-config.yaml* file:

```yaml
-   repo: https://github.com/saroad2/statue
    hooks:
    -   id: statue
```

If you're using the default template as configuration, we highly recommend adding the `--context=fast` or
`--context=format` flags for a quicker committing. For the other checks you can run *Statue* directly.  