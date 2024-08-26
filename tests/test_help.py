# pylint: disable=missing-module-docstring missing-function-docstring
import pytest
from dotenv import load_dotenv

from .ctx import get_ipython_shell

load_dotenv()


@pytest.fixture(name="ipython_shell", scope="module")
def fixture_ipython_shell():
    return get_ipython_shell()


def test_no_command(ipython_shell, capsys):
    # Arrange
    expected_output = \
        """Available commands: get-context, search
Usage:
%cluedin get-context --jwt <jwt>
%cluedin search --context <context> --query <query> [--limit <limit>]
"""

    # Act
    context = ipython_shell.run_line_magic('cluedin', '')

    # Assert
    assert context is None
    assert expected_output == capsys.readouterr().out


def test_unknown_command_with_args(ipython_shell, capsys):
    # Arrange
    expected_output = \
        """Unknown command: "foobar".
Available commands: get-context, search
Usage:
%cluedin get-context --jwt <jwt>
%cluedin search --context <context> --query <query> [--limit <limit>]
"""

    # Act
    context = ipython_shell.run_line_magic('cluedin', 'foobar --help')

    # Assert
    assert context is None
    assert expected_output == capsys.readouterr().out


def test_help(ipython_shell, capsys):
    # Arrange
    expected_output = \
        """Available commands: get-context, search
Usage:
%cluedin get-context --jwt <jwt>
%cluedin search --context <context> --query <query> [--limit <limit>]
"""

    # Act
    context = ipython_shell.run_line_magic('cluedin', '--help')

    # Assert
    assert context is None
    assert expected_output == capsys.readouterr().out
