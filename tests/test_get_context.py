# pylint: disable=missing-module-docstring missing-function-docstring
import os

import pytest
from dotenv import load_dotenv

from .ctx import get_ipython_shell

load_dotenv()


@pytest.fixture(name="ipython_shell", scope="module")
def fixture_ipython_shell():
    return get_ipython_shell()


def test_get_context_success(ipython_shell):
    # Arrange
    line = f'get-context --jwt {os.getenv("ACCESS_TOKEN")}'

    # Act
    context = ipython_shell.run_line_magic('cluedin', line)

    # Assert
    assert context.protocol == 'https'
    assert context.domain == '172.167.52.102.sslip.io'
    assert context.org_name == 'foobar'
    assert context.access_token == os.getenv('ACCESS_TOKEN')


def test_get_context_failure(ipython_shell, capsys):
    # Arrange
    line = 'get-context --jwt invalid_token'

    # Act
    context = ipython_shell.run_line_magic('cluedin', line)

    # Assert
    assert context is None
    assert \
        'not enough values to unpack (expected 3, got 1)\n' == \
        capsys.readouterr().out
