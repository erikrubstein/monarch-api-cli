# AGENTS.md

## Purpose

This repository contains an installable CLI for the published `monarch-api` Python client. The public project name is `monarch-api-cli`, while the installed command is `monarch`.

## Core Rules

- Keep the maintained implementation under `src/monarch_cli/`.
- Preserve the current command surface unless a change is explicitly requested.
- Prefer splitting logic by concern instead of growing a new monolithic module.
- Keep request payloads and CLI flags close to the underlying `monarch-api` surface.

## Project Layout

- `src/monarch_cli/`
  - `parser.py`: argparse wiring and command tree construction
  - `commands.py`: command handlers
  - `builders.py`: request payload builders from CLI args
  - `summaries.py`: summarized output shaping
  - `runtime.py`: session handling, JSON loading, console helpers
  - `style.py`: help formatting and colorized output
- `tests/`
  - payload-building and CLI-focused tests

## Testing

- Prefer mocked or argument-level tests over live account mutations.
- Do not run destructive live operations against a real Monarch account unless explicitly asked.
- Before release-related changes, run:
  - `python -m pytest`
  - `python -m build`
  - `python -m twine check dist/*`

## Documentation

- Keep `README.md` as the primary public-facing documentation.
- Keep install instructions, release steps, and naming decisions in `README.md` unless the repo grows enough to justify dedicated docs.
- Update `README.md` when changing the command name, install method, session path, or packaging metadata.

## Releases

- The PyPI distribution name is `monarch-api-cli`.
- The installed console command is `monarch`.
- Add real `[project.urls]` metadata in `pyproject.toml` once the public GitHub repo exists.
- Keep GitHub releases and PyPI releases aligned by version tag.

## Style

- Keep changes pragmatic and minimal.
- Prefer direct, readable argparse wiring over clever abstractions.
- Avoid introducing framework dependencies unless there is a clear benefit.
