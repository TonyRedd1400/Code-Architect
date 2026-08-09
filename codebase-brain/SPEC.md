# codebase-brain Specification

## Vision

Transform any code repository into a structured, queryable knowledge base that enables AI agents to understand, navigate, and reason about codebases without prior context.

## MVP Scope

The Minimum Viable Product (MVP) will be a Python CLI tool that:

1. **Scans** a local repository and identifies files, languages, and structure
2. **Detects** entrypoints, scripts, and basic metadata (package.json, setup.py, etc.)
3. **Indexes** files and basic symbols in a SQLite database
4. **Builds** a simple dependency graph between files and modules
5. **Provides** CLI commands for:
   - `analyze`: Full repository analysis
   - `overview`: High-level summary of the repository
   - `explain`: Explain a specific file or module
   - `impact`: Show what depends on a target (basic)
   - `find`: Search for files or symbols

### In Scope for MVP

- Local repository analysis only
- SQLite database (file-based, no server)
- Basic file scanning with ignore patterns
- Language detection by extension and content hints
- Entrypoint detection for common patterns (package.json main, setup.py, etc.)
- Simple symbol extraction (function/class names via regex)
- Basic dependency graph (file-level imports)
- CLI with argparse
- pytest test suite

### Out of Scope (Not Now)

- LLM integration or calls
- Tree-sitter or advanced parsing
- Vector databases or embeddings
- Neo4j or graph databases
- Runtime tracing or execution
- Web UI or frontend
- Microservices architecture
- External API integrations (GitHub, etc.)
- Docker containers
- Remote databases
- Autonomous agents
- Semantic code analysis
- Type inference
- Cross-repository analysis

## Assumptions

1. Repositories are accessible locally via filesystem
2. Python 3.11+ is available
3. SQLite is available (standard library)
4. Users run the CLI directly (no service deployment)
5. Analysis is read-only (no modifications to target repos)

## Risks

| Risk | Mitigation |
|------|------------|
| Parsing complexity grows too fast | Start with regex-based extraction, defer tree-sitter |
| Database schema needs frequent changes | Keep schema simple initially, version it |
| Performance issues on large repos | Implement streaming, batch operations |
| Too many language-specific edge cases | Focus on top 5 languages first (JS, Python, Java, Go, Rust) |

## Acceptance Criteria for MVP

- [ ] CLI installs via `pip install -e .`
- [ ] All 5 subcommands exist and show help without errors
- [ ] `codebrain analyze <path>` scans repo and creates SQLite DB
- [ ] `codebrain overview <path>` shows basic repo statistics
- [ ] `codebrain explain <path> <file>` shows file info (placeholder OK)
- [ ] `codebrain impact <path> <target>` shows dependents (basic)
- [ ] `codebrain find <path> <query>` searches files (basic)
- [ ] SQLite database created with required tables
- [ ] Tests pass with `pytest`
- [ ] No external service dependencies
- [ ] No LLM calls made

## Success Metrics

- CLI responds to all commands without crashing
- Database schema supports future expansion
- Test coverage > 60% for core modules
- Clean architecture allowing incremental development
