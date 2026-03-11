# CLAUDE.md — Hello World

## Project Overview

Hello World is a **demo autonomous service** built on the [Open Autonomy](https://stack.olas.network/open-autonomy/) framework. It showcases the basic structure and lifecycle of an ABCI-based multi-agent service using the OLAS stack (AEA + Tendermint consensus).

**Reference repo:** [valory-xyz/trader](https://github.com/valory-xyz/trader) (develop branch) — follow the same patterns for CI, tox, and package structure.

## What the Service Does

A minimal "hello world" service that demonstrates:

- Agent registration and round-based consensus
- FSM (Finite State Machine) transitions via ABCI
- Transaction settlement through a multisig Safe
- The compose pattern for chaining sub-skills

## Repository Structure

```text
packages/valory/
├── skills/
│   └── hello_world_abci/           # Core skill: hello world FSM
├── agents/
│   └── hello_world/                # Agent configuration
└── services/
    └── hello_world/                # Service configuration
```

### What you own vs. what is synced

Package ownership is defined in `packages/packages.json`:

- **`dev`** section: project-specific packages (owned by this repo, committed to git):
  - `skill/valory/hello_world_abci/0.1.0`
  - `agent/valory/hello_world/0.1.0`
  - `service/valory/hello_world/0.1.0`

- **`third_party`** section: dependencies synced from IPFS via `autonomy packages sync --all`. Do not modify these directly — they are not committed to git.

## Development Commands

### Prerequisites

- Python 3.10–3.14
- [tox](https://tox.wiki/)
- [tomte](https://github.com/valory-xyz/tomte) (installed via tox deps)

### Setup

This repo uses `Pipfile` (not `pyproject.toml` with Poetry):

```bash
pipenv install --dev
```

### Syncing third-party packages

Before running tests, sync all AEA packages from IPFS:

```bash
autonomy init --reset --author ci --remote --ipfs --ipfs-node "/dns/registry.autonolas.tech/tcp/443/https"
autonomy packages sync --all
```

This is done automatically by tox test environments.

### Running tests

```bash
# Run all unit tests (Linux, Python 3.11)
tox -e py3.11-linux

# Recreate tox virtualenv (clear cache)
tox -e py3.11-linux -r
```

Test environments follow the pattern `py{version}-{platform}` where platform is `linux`, `win`, or `darwin`.

### Formatting (auto-fix)

```bash
tox -e black && tox -e isort
```

### Locking packages

After modifying any dev package, update the package hashes:

```bash
autonomy packages lock
```

### Linting & static analysis

```bash
tox -e black-check    # Code formatting check
tox -e isort-check    # Import sorting check
tox -e flake8         # Linting
tox -e mypy           # Type checking
tox -e pylint         # Pylint
tox -e darglint       # Docstring linting
tox -e bandit         # Security linting
tox -e safety         # Dependency vulnerability check
tox -e liccheck       # License compliance check
```

### Package integrity

```bash
tox -e check-hash           # Verify package hashes
tox -e check-packages       # Validate package structure
tox -e check-abciapp-specs  # Validate FSM specifications
```

## CI

CI workflows: `.github/workflows/workflow.yml`, `.github/workflows/release.yml`

- Cross-platform matrix: Ubuntu, macOS, Windows
- Python versions: 3.10–3.14
- Uses `tomte[tox]` for test orchestration

## Key Gotchas

### Third-party packages are not committed

Packages synced via `autonomy packages sync --all` are fetched from IPFS at test time. They appear in `packages/` but are in `.gitignore`. Do not commit them.

### `Pipfile` not `pyproject.toml`

This repo uses `Pipfile`/`Pipfile.lock` for dependency management, not Poetry. Version pins live in both `Pipfile` and `tox.ini`.

### tox cache

If you get stale dependency errors, clear tox cache: `rm -rf .tox` or use `tox -e <env> -r`.

## Third-party Dependency Repositories

This repo depends on third-party AEA packages sourced from these upstream repositories. When bumping the open-autonomy framework version, each upstream repo must be checked for a compatible release tag:

| Repository | What it provides |
|------------|-----------------|
| [open-autonomy](https://github.com/valory-xyz/open-autonomy) | Core framework: abstract_round_abci, registration, transaction_settlement, reset_pause, termination |
| [open-aea](https://github.com/valory-xyz/open-aea) | AEA framework: protocols (contract_api, ledger_api, http, signing, etc.), connections, base contracts (gnosis_safe, multisend, service_registry) |

## Commit Conventions

Follow conventional commits: `feat:`, `fix:`, `chore:`, `docs:`, `test:`, `refactor:`
