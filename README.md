# CluedIn IPython magic commands

This module provides IPython [magic](https://ipython.readthedocs.io/en/stable/interactive/python-ipython-diff.html#magics) commands for interacting with the CluedIn API.

```python
# Install the package.
%pip install cluedin-magic
```

```python
# Load the extension.
%load_ext cluedin_magic
```

```python
# Create a new CluedIn context from a JWT token.
api_token = '<your_token_here>'
ctx = %cluedin get-context --jwt %api_token
```

```python
# Find all entities with a specific entityType.
%cluedin search --context ctx --query +entityType:/Infrastructure/User
```

```python
# Find all entities with a specific entityType and limit the results.
%cluedin search --context ctx --query +entityType:/Infrastructure/User --limit 10
```

```python
# Complex query with multiple properties and limit the results.
%cluedin search --context ctx --query +entityType:/IMDb/Name -properties.imdb.name.deathYear:"\\\\N" --limit 10
```

```python
# Save the results of a query to a pandas DataFrame.
pd = %cluedin search --context ctx --query +entityType:/IMDb/Name +properties.imdb.name.birthYear:1981
```