from .cluedin_magic import CluedInMagics


def load_ipython_extension(ipython):
    ipython.register_magics(CluedInMagics)
