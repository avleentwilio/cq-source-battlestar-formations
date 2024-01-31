# Cloudquery plugin to get deployments, plans and formations from Battlestar

## How to use

Make a copy of `TestConfig.yaml` called `LocalConfig.yaml` and add a username
and password. This file will be ignored by git.

Install the required local environment:
```
pip install .
```
Install the cloudquery binary:
```
brew install cloudquery/tap/cloudquery
```
Run the sync:
```
cloudquery sync LocalConfig.yaml
```
The results can be found in `db.sqlite`.

## How this sync works

The tables for the database are defined in the `plugin/tables/` directory. Each
table has a `TableResolver`. This calls an iterator which does the actual
fetching and manipulating of data.

The iterators are defined in `plugin/formations/formation.py`.

## Child tables

There is a parent-child relationship between the `deployments` and `plans`
tables. The `/v1/Deployments` battlestar API returns a `plans` hash which needs
to be stored separately.
This relationship is defined in `plugin/tables/deployments.py` after the list of
columns, and activated at the end of the file in the `child_resolvers()` method.
