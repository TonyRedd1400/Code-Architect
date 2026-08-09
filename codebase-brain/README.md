# codebase-brain

Convert a code repository into a navigable knowledge base for AI agents.

## Current Status

**Status:** Initial skeleton / MVP development

This is the initial skeleton of the project. The CLI structure is in place with placeholder commands. Next steps include implementing basic repository scanning and language detection.

## Installation

```bash
cd codebase-brain
pip install -e .
```

## Running Tests

```bash
pytest
```

## CLI Usage

```bash
# Show help
codebrain --help

# Analyze a repository
codebrain analyze <repo_path>

# Get overview of a repository
codebrain overview <repo_path>

# Explain a specific file or module
codebrain explain <repo_path> <target_path>

# Analyze impact of changes
codebrain impact <repo_path> <target>

# Find something in the codebase
codebrain find <repo_path> <query>
```

## Next Steps

1. Implement basic language detection
2. Implement file scanning (ignoring node_modules, dist, .git, etc.)
3. Implement package.json detection
4. Implement entrypoint detection
5. Create SQLite database with initial schema
6. Build basic dependency graph
7. Implement overview command
8. Implement simple impact analysis

See `TASKS.md` for detailed task breakdown.

## Project Structure

```
codebase-brain/
  src/codebase_brain/    # Main source code
  tests/                 # Test suite
  prompts/               # LLM prompts for future use
  docs/                  # Documentation
```

## License

MIT
