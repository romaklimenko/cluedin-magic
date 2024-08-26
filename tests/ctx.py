# pylint: disable=missing-module-docstring missing-function-docstring
import os
import sys

from IPython.terminal.interactiveshell import TerminalInteractiveShell

from cluedin_magic.cluedin_magic import CluedInMagics

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))


def get_ipython_shell():
    ip = TerminalInteractiveShell.instance()
    ip.register_magics(CluedInMagics)
    return ip
