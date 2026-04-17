# monarch-api-cli

Installable command-line interface for the published [`monarch-api`](https://pypi.org/project/monarch-api/) Python client.

This repository is intended to become the public home of the CLI. The repository name and PyPI distribution name are both `monarch-api-cli`, while the installed command is simply `monarch`.

The package is organized as a real `src/` application now:

- `src/monarch_cli/` contains the maintained CLI implementation.
- `tests/` covers payload-building behavior.

## Install

From PyPI, the intended distribution name is:

```bash
pip install monarch-api-cli
```

With `pipx`:

```bash
pipx install monarch-api-cli
```

For local development:

```bash
pip install -e .[dev]
```

## Usage

The primary console command is `monarch`:

```bash
monarch --help
monarch --help all
monarch household preferences
monarch transactions create --help
```

The saved session is stored at:

```text
~/.monarch-api-cli/monarch_session.json
```

Older sessions from `~/.monarch-cli/monarch_session.json` are still accepted and migrated forward on use.

## Notes

- `monarch-api` remains the underlying Python client, imported as `monarch_api`.
- `monarch-api-cli` is the public repository and PyPI distribution for the CLI.
- The installed command remains `monarch`.

## Development

```bash
pip install -e .[dev]
python -m pytest
python -m build
python -m twine check dist/*
```

## AI Skills

Repo-local agent skills live under `skills/`.

- `skills/monarch-finance-ops/` provides a reusable skill for analyzing, reconciling, budgeting, and safely managing Monarch financial data through this CLI.

## Release

This project publishes the PyPI distribution `monarch-api-cli` and installs the console command `monarch`.

Before the first public release:

1. Create the `monarch-api-cli` project on PyPI if it does not already exist.
2. Configure PyPI Trusted Publishing for this repository.

For each release:

1. Update `version` in `pyproject.toml`.
2. Run verification:

```bash
python -m pip install -e .[dev]
python -m pytest
python -m build
python -m twine check dist/*
```

3. Commit the release changes.
4. Tag and push the release:

```bash
git tag v0.1.0
git push origin main --tags
```

5. Create a GitHub release for the tag.
6. The `Publish To PyPI` workflow will publish automatically if Trusted Publishing is configured.
