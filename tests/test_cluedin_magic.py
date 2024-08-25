"""Test the CluedInMagics class."""
import pytest
from IPython.terminal.interactiveshell import TerminalInteractiveShell

from cluedin_magic.cluedin_magic import CluedInMagics

# pylint: disable=line-too-long
ACCESS_TOKEN = 'eyJhbGciOiJSUzI1NiIsImtpZCI6IkRFMTA3RkQ4RTg3MjlBMkFENzBDNEU2RjJFQTNDMUU1RDk0RjdDREFSUzI1NiIsInR5cCI6ImF0K2p3dCIsIng1dCI6IjNoQl8yT2h5bWlyWERFNXZMcVBCNWRsUGZObyJ9.eyJuYmYiOjE3MjM3MjQwODEsImV4cCI6MTc1NTMwMzI3OSwiaXNzIjoiaHR0cHM6Ly9hcHAuMTcyLjE2Ny41Mi4xMDIuc3NsaXAuaW8vYXV0aC8iLCJhdWQiOlsiU2VydmVyQXBpRm9yVUkiLCJQdWJsaWNBcGkiXSwiY2xpZW50X2lkIjoiUHVibGljQXBpQ2xpZW50Iiwicm9sZSI6IkFQSSIsIkNsaWVudElkIjoiZm9vYmFyIiwiT3JnYW5pemF0aW9uSWQiOiI2YzFiNzE4Ny1jZjI3LTQ0YzYtYTQwNC02OTgwMmRmOTY0N2EiLCJPcmdhbml6YXRpb25OYW1lIjoiZm9vYmFyIiwiT3JnYW5pemF0aW9uQ2xpZW50UmVmZXJlbmNlIjoiZm9vYmFyIiwiSWQiOiI2MmY0MDg5OC0zOTY0LTRiNDktYWIyNi1iN2EwMTkyYmFiNWYiLCJhcGkiOiIyOTVmYTc5Mi1jYzljLTRlM2ItYmIzYy0xNWVhYzJhMDZjYTEiLCJqdGkiOiJGODYzQzk2NTIwMzczODQ0NUE5OTA2RUYzMkNGODg3QSIsImlhdCI6MTcyMzcyNDA4MSwic2NvcGUiOlsiUHVibGljQXBpIiwiU2VydmVyQXBpRm9yVUkiXX0.Po1E88vS1YEDRQOz0EEBwxNvyLPrDIDJRXzzc0cQCBfiAmWXG_k3F4Q1VrRidwrDnCtR7OUS5412j_894ynn0veF9leynt1QiapZescxHfLdqJ8Bcq6ocn330Zvm_gKi-O0coOIkQOzCy__X7kxSrbrdFwVjXicsLafTNNqwHgcWufcFqD0nPdu9jzk7RsEKkscg-l83MBVDgXaHcB4qZwqlAUb_NOruGbozTh9VZzxJGpRVvTki0VcVGOc8papKCECE5p-N4AAWbM3zUeSBHigGJ8EBHXS3mGq9ezuRL5Vr2bWr7GrtujZDOEMsLtNaYq4KBVkAPGB-P_JqF2uI_A'


@pytest.fixture(name="ipython_shell", scope="module")
def fixture_ipython_shell():
    """Fixture to set up the IPython shell and register the magic."""
    ip = TerminalInteractiveShell.instance()
    ip.register_magics(CluedInMagics)
    return ip

def test_no_op(ipython_shell):
    """Test the cluedin magic with an invalid command."""
    # Arrange
    line = 'invalid-command'
    # Act
    result = ipython_shell.run_line_magic('cluedin', line)
    # Assert
    assert 'Usage:' in result

def test_get_credentials_success(ipython_shell):
    """Test the get-context magic with a valid access token."""

    # Arrange
    line = f'get-context {ACCESS_TOKEN}'

    # Act
    context = ipython_shell.run_line_magic('cluedin', line)

    # Assert
    assert context.protocol == 'https'
    assert context.domain == '172.167.52.102.sslip.io'
    assert context.org_name == 'foobar'
    assert context.access_token == ACCESS_TOKEN


def test_get_credentials_failure(ipython_shell, capsys):
    """Test the get-context magic with an invalid access token."""

    # Arrange
    line = 'get-context invalid_token'

    # Act
    context = ipython_shell.run_line_magic('cluedin', line)

    # Assert
    assert context is None
    assert \
        'not enough values to unpack (expected 3, got 1)\n' == \
        capsys.readouterr().out
