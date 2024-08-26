# pylint: disable=missing-module-docstring missing-function-docstring
from cluedin_magic.cluedin_magic import CluedInMagics


def test_empty_param():
    # Arrange
    # Act
    actual = CluedInMagics.parse_params('--help')
    # Assert
    assert actual['help'] == ''


def test_non_empty_param():
    # Arrange
    # Act
    actual = CluedInMagics.parse_params(
        '--query +entityType:/Infrastructure/User')
    # Assert
    assert actual['query'] == '+entityType:/Infrastructure/User'


def test_multiple_params():
    # Arrange
    # Act
    actual = CluedInMagics.parse_params(
        '--query +entityType:/IMDb/Name -properties.imdb.name.deathYear:*')
    # Assert
    assert actual['query'] == '+entityType:/IMDb/Name -properties.imdb.name.deathYear:*'


def test_complex_params():
    # Arrange
    # Act
    actual = CluedInMagics.parse_params(
        # pylint: disable=line-too-long
        'search --context ctx --query +entityType:/IMDb/Name -properties.imdb.name.deathYear:"\\\\N" +name:"John Refoua"')
    # Assert
    # pylint: disable=line-too-long
    assert actual['query'] == '+entityType:/IMDb/Name -properties.imdb.name.deathYear:"\\\\N" +name:"John Refoua"'
