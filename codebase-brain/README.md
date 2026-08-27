# codebase-brain

Convert a local code repository into a file-level SQLite knowledge base for AI agents.

## Current status

The foundational MVP flow is functional:

- `analyze` scans a repository, detects languages and entrypoints, and persists files and metadata.
- `overview` prints live repository statistics.
- SQLite databases are stored outside the analyzed repository by default.
- `explain`, `impact`, and `find` remain intentionally unimplemented and return a non-zero exit code.
- Dependency edges, symbol extraction, and LLM integration are future work.

## Installation

Python 3.11 or newer is required.

```bash
cd codebase-brain
pip install -e ".[dev]"
```

## Tests

```bash
pytest
```

## CLI usage

```bash
# Show help
codebrain --help

# Analyze a repository using the platform user cache
codebrain analyze <repo_path>

# Choose an explicit SQLite output path
codebrain analyze <repo_path> --db-path ./analysis.db

# Print a live overview without writing to the repository
codebrain overview <repo_path>
```

The default database directory is `%LOCALAPPDATA%/codebase-brain` on Windows,
`$XDG_CACHE_HOME/codebase-brain` when configured, or `~/.cache/codebase-brain`
otherwise. The filename includes a hash of the absolute repository path so
repositories with the same directory name do not collide.

## Current data flow

```text
repository -> scan/language/entrypoint detection -> external SQLite database
           -> live overview
```

See `SPEC.md`, `ARCHITECTURE.md`, and `TASKS.md` for scope and future work.

## License

MIT
