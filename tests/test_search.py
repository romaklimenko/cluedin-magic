# pylint: disable=missing-module-docstring missing-function-docstring
import os

import pytest
from dotenv import load_dotenv

from .ctx import get_ipython_shell

load_dotenv()


@pytest.fixture(name="ipython_shell", scope="module")
def fixture_ipython_shell():
    return get_ipython_shell()


def test_get_search_without_limit(ipython_shell):
    # Arrange
    ipython_shell.run_cell(
        f"ctx = %cluedin get-context --jwt {os.getenv('ACCESS_TOKEN')}")
    line = 'search --context ctx --query +entityType:/Infrastructure/User'
    # Act
    df = ipython_shell.run_line_magic('cluedin', line)
    # Assert
    assert len(df) == 1


def test_get_search_with_limit(ipython_shell):
    # Arrange
    ipython_shell.run_cell(
        f"ctx = %cluedin get-context --jwt {os.getenv('ACCESS_TOKEN')}")
    line = 'search --context ctx --query +entityType:/IMDb/Name --limit 10'
    # Act
    df = ipython_shell.run_line_magic('cluedin', line)
    # Assert
    assert len(df) == 10


def test_get_search_negative_condition(ipython_shell):
    # Arrange
    ipython_shell.run_cell(
        f"ctx = %cluedin get-context --jwt {os.getenv('ACCESS_TOKEN')}")
    line = 'search --context ctx --query -entityType:/IMDb/Name --limit 10'
    # Act
    df = ipython_shell.run_line_magic('cluedin', line)
    # Assert
    assert len(df) == 2


def test_get_search_multiple_conditions_one(ipython_shell):
    # Arrange
    ipython_shell.run_cell(
        f"ctx = %cluedin get-context --jwt {os.getenv('ACCESS_TOKEN')}")
    line = 'search --context ctx --query +entityType:/IMDb/Name -properties.imdb.name.deathYear:"\\\\N" +name:"John Refoua"'
    # Act
    df = ipython_shell.run_line_magic('cluedin', line)
    # Assert
    assert len(df) == 1


def test_get_search_multiple_conditions_limit(ipython_shell):
    # Arrange
    ipython_shell.run_cell(
        f"ctx = %cluedin get-context --jwt {os.getenv('ACCESS_TOKEN')}")
    # pylint: disable=line-too-long
    line = 'search --context ctx --query +entityType:/IMDb/Name -properties.imdb.name.deathYear:"\\\\N" --limit 1000'
    # Act
    df = ipython_shell.run_line_magic('cluedin', line)
    # Assert
    assert len(df) == 1000


def test_get_search_multiple_conditions_no_limit(ipython_shell):
    # Arrange
    ipython_shell.run_cell(
        f"ctx = %cluedin get-context --jwt {os.getenv('ACCESS_TOKEN')}")
    # pylint: disable=line-too-long
    line = 'search --context ctx --query +entityType:/IMDb/Name -properties.imdb.name.deathYear:"\\\\N"'
    # Act
    df = ipython_shell.run_line_magic('cluedin', line)
    # Assert
    assert len(df) == 53729
