# Changelog

All notable changes to python-relations-postgresql are recorded here, newest first. Format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow [SemVer](https://semver.org/).

## [Unreleased]

## [0.6.3] - 2026-06-06

- Bumped the `relations-sql` requirement to 0.6.8 and `relations-dil` to 0.6.14, supporting many-to-many relations.
- Installed git in the Dockerfile; tests in `test_table.py` were updated.

## [0.6.2] - 2022-11-25

- Switched to the PyPI `relations-sql` release (0.6.7) and required `relations-dil` 0.6.12 in the requirements file.
- Renamed the distribution to `relations-postgresql`.

## [0.6.1] - 2022-08-06

- Prepared the package for PyPI with a `LICENSE.txt`, a `PYPI.md` description, and `testpypi` and `pypi` Makefile targets.
- Removed the git-based installs from the setup step.

## [0.6.0] - 2022-03-14

- Fixed index renames: the `INDEX` class now generates `ALTER INDEX name RENAME TO new_name` with a dedicated `modify` method.
- Fixed table migrations: the `TABLE` class `name` method now handles separate migration and definition names and schemas, and a new `store` method generates the rename or schema change.
- Updated dependencies to `python-relations` 0.6.9 and `relations-sql` 0.6.5, and replaced the psycopg2 test module with an execute test module.

## [0.5.0] - 2022-03-13

- Updated the `python-relations` requirement to 0.6.8 and `relations-sql` to 0.6.4, adding support for familial access.

## [0.4.0] - 2022-02-18

- Updated the `python-relations` requirement to 0.6.7 and `relations-sql` to 0.6.3, which changed labels to titles.

## [0.3.0] - 2021-11-21

- Renamed the package to `python-relations-postgresql` and moved its dependencies to the relations-dil organization (`python-relations` 0.6.6, `relations-sql` 0.6.2).

## [0.2.0] - 2021-11-13

- Updated the `python-relations` requirement to 0.6.5 and `relations-sql` to 0.6.1 after the library renames.

## [0.1.0] - 2021-11-12

- Initial release of the PostgreSQL dialect for `relations-sql`, providing PostgreSQL versions of the expression, criterion, criteria, clause and query classes.
- Added PostgreSQL DDL classes for `COLUMN`, `INDEX` and `TABLE`, with `BIGSERIAL` for auto ids, generated stored columns for extracted values, and default and not-null alter statements.
- Included execution tests against a PostgreSQL server, a `postgres.sh` helper, and Dockerfile, Jenkinsfile and Makefile.
