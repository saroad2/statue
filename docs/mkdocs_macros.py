import statue


def define_env(env):

    @env.macro
    def version():
        return statue.__version__
