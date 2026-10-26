# Changelog

All notable changes to python-relations-postgresql are recorded here, newest first. Format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow [SemVer](https://semver.org/).

## [Unreleased]

### Added
- Jenkins releases on a merge to `main`: a `release` stage (only on `main`) runs `make release`, which does nothing for a version that is already released and otherwise does the test release, the release and the tag. It pushes the tag with the `github` credential, as Leroy Jenkins, one build at a time, with a two hour timeout (relations-dil/python-relations#80). The package builds run in a copy with only the files they use mounted read-only, so nothing root-owned is left in the workspace, and `make tag` stops on a failure instead of ignoring it. The release scripts work with the older git on the Jenkins host.
- `make help` lists every target with what it does (each target has a `## description` after it), and is what a bare `make` runs.
- Release tooling, the same as relations-dil's (relations-dil/python-relations#77): `make new` starts a release, `make version` sets the version, `make release-check` says where a release is up to and what would stop it, `make release` does what's left (checks, TestPyPI and a clean install from it, PyPI, the tag), `make dist-check` builds and checks the distributions, and `make test-release` tests the scripts against a throwaway repo and fake indexes. The work is in `scripts/`.
- A `VERSION` file as the one place the version is set: the `Makefile` reads it and mounts it, `testpypi` and `pypi` pass it as `BUILD_VERSION`, and `setup.py` reads `BUILD_VERSION` or the file.

### Changed
- A str field's `length` is honored: it makes the column `VARCHAR(length)` when created, added or changed, instead of always `VARCHAR(255)`, which stays the default for a str with no length. Anything that isn't a str ignores `length` (relations-dil/python-relations-postgresql#15).
- `make release-check` and `make release` don't run `build`, `test`, `lint` and `setup` again: the Jenkins stages have just run them before the release stage, so it was the same work twice. Run them yourself before checking by hand, as `make release-check` is only the checks and `dist-check` now (relations-dil/python-relations#90).
- Every `docker run` in the `Makefile` uses `--rm`, and a replaced database container is removed with its volume (`docker rm --force -v`), so builds and test runs leave no stopped containers or volumes behind.
- `testpypi` and `pypi` run in the current `python` image with `build` and `twine` installed on the fly, so the custom `gaf3/pypi` image is no longer used.

## [0.6.4] - 2026-10-14

### Fixed
- Changing an id from an auto int to a string (relations-dil 0.6.18) drops the sequence default `BIGSERIAL` gave it, whether the migration says `auto` is gone or only changes the kind. It used to keep `DEFAULT nextval(...)`, so an insert without an id got the next number as a string instead of being refused as `NOT NULL`. Needs relations-sql 0.6.10, which sees a change to `auto`.

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
