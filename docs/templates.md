# Out-Of-The-Box Templates

This file contains all the out-of-the-box templates provided by *Statue*. At this time *Statue* supports
only a single template, which is the default template. This will be changed in the future.

## Default Template

### Contexts
{% for context in default_template().contexts_repository %}
#### {{ context.name }}
{{ context.help }}
{% if context.aliases|length != 0 %}
*Aliases*: {{ bold_list(context.aliases) }}
{% endif %}
{% if context.parent is not none %} 
*Parent*: {{ link("templates", context.parent.name) }}
{% endif %}
{% endfor %}
{% if context.allowed_by_default %}*Allowed by default*.{% endif %}

### Commands
{% for command_builder in default_template().commands_repository %}
#### {{ command_builder.name }}
{{ command_builder.help }}

*Default Arguments*: `{{ command_builder.name }} <source> {{ " ".join(command_builder.default_args)}}`
{% if command_builder.required_contexts | length != 0 %} 
*Required Contexts*: {{ contexts_links_list("templates", command_builder.required_contexts) }}
{% endif %}
{% if command_builder.allowed_contexts | length != 0 %} 
*Allowed Contexts*: {{ contexts_links_list("templates", command_builder.allowed_contexts) }}
{% endif %}
{% if command_builder.specified_contexts | length != 0 %}
*Specified contexts*:
{% for context, context_specification in command_builder.contexts_specifications.items()%}
* {{ link("templates", context.name) }}: {{ format_specification(context_specification) }}
{% endfor %}
{% endif %}
{% endfor %}

