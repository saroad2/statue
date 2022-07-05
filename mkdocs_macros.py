from statue import __version__
from statue.config.configuration import Configuration
from statue.constants import DEFAULT_HISTORY_SIZE
from statue.templates.templates_provider import TemplatesProvider

DEFAULT_TEMPLATE = Configuration.from_file(
    TemplatesProvider.get_template_path("defaults")
)


def define_env(env):
    @env.macro
    def version():
        return __version__

    @env.macro
    def history_size():
        return DEFAULT_HISTORY_SIZE

    @env.macro
    def default_template():
        return DEFAULT_TEMPLATE

    @env.macro
    def bold_list(items):
        return ", ".join(f"**{item}**" for item in items)

    @env.macro
    def link(filename, title):
        return f"**[{title}]({filename}.md#{title})**"

    @env.macro
    def contexts_links_list(filename, items):
        return ", ".join(link(filename, item.name) for item in items)

    @env.macro
    def format_specification(context_specification):
        if context_specification.clear_args:
            return "Clears arguments"
        if context_specification.add_args:
            return f"Adds arguments `{' '.join(context_specification.add_args)}`"
        return f"Overrides arguments with `{' '.join(context_specification.args)}`"
