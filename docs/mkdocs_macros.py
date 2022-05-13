from statue import __version__
from statue.constants import DEFAULT_HISTORY_SIZE


def define_env(env):
    @env.macro
    def version():
        return __version__

    @env.macro
    def history_size():
        return DEFAULT_HISTORY_SIZE
