# Tasks - codebase-brain MVP

## Priority 1: Foundation

### Task 1.1: File Scanning with Ignore Patterns
**Description:** Implement `scan_repository(path)` that walks the directory tree and collects file information while ignoring common directories.

**Acceptance Criteria:**
- Ignores: `node_modules`, `dist`, `build`, `.git`, `coverage`, `__pycache__`, `.venv`, `venv`
- Returns list of files with path, size, extension
- Handles symlinks gracefully (skip or follow with limit)
- Works on repos with 10k+ files without memory issues

**Priority:** P0

---

### Task 1.2: Language Detection
**Description:** Implement `detect_languages(path)` that identifies programming languages in the repository.

**Acceptance Criteria:**
- Detects by file extension (.py, .js, .ts, .java, .go, .rs, etc.)
- Detects by shebang for script files
- Detects by content hints (e.g., `import` statements)
- Returns dict: `{language: count}` or list of detected languages
- Supports at least 10 common languages

**Priority:** P0

---

### Task 1.3: Package.json Detection
**Description:** Detect and parse package.json files to extract metadata, scripts, and dependencies.

**Acceptance Criteria:**
- Finds all package.json files
- Extracts: name, version, main, scripts, dependencies, devDependencies
- Identifies entrypoint from "main" field
- Lists available npm scripts

**Priority:** P0

---

### Task 1.4: Entrypoint Detection
**Description:** Implement `detect_entrypoints(path)` for multiple ecosystems.

**Acceptance Criteria:**
- JavaScript/Node: package.json main, index.js
- Python: setup.py, pyproject.toml, __main__.py
- Java: pom.xml, build.gradle main class
- Go: main.go, main package
- Rust: Cargo.toml, src/main.rs
- Returns list of entrypoint files with type

**Priority:** P1

---

### Task 1.5: SQLite Schema Creation
**Description:** Create initial database schema with all required tables.

**Acceptance Criteria:**
- Tables: repos, files, symbols, edges, summaries, metadata
- Foreign keys enabled
- Indexes on commonly queried columns
- Schema version tracked
- Function `create_tables(conn)` works on fresh DB

**Priority:** P0

---

## Priority 2: Core Analysis

### Task 2.1: File Indexing
**Description:** Insert scanned files into SQLite database.

**Acceptance Criteria:**
- Batch inserts for performance
- Stores: path, language, size_bytes, hash (optional)
- Links files to repo_id
- Handles updates (re-analysis)

**Priority:** P1

---

### Task 2.2: Basic Symbol Extraction
**Description:** Extract function and class names using regex patterns.

**Acceptance Criteria:**
- Python: `def func()`, `class Class:`
- JavaScript: `function func()`, `const func =`, `class Class`
- Stores: name, kind (function/class), line numbers
- One symbol per row in `symbols` table

**Priority:** P1

---

### Task 2.3: Import/Dependency Graph
**Description:** Build file-level dependency graph from import statements.

**Acceptance Criteria:**
- Python: `import x`, `from x import y`
- JavaScript: `import`, `require()`
- Creates edges in `edges` table
- Relation types: imports, depends_on

**Priority:** P1

---

### Task 2.4: Overview Command
**Description:** Implement `codebrain overview <repo_path>` with real data.

**Acceptance Criteria:**
- Shows: total files, languages breakdown, top directories
- Shows: entrypoints found, scripts available
- Shows: total symbols, total dependencies
- Output in readable format (text table or JSON)

**Priority:** P1

---

## Priority 3: Query & Impact

### Task 3.1: Impact Analysis (Basic)
**Description:** Implement `codebrain impact <path> <target>` showing what depends on target.

**Acceptance Criteria:**
- Given a file path, find all files that import it
- Uses edges table for reverse lookup
- Shows direct dependents only (MVP)
- Optional: show transitive dependents

**Priority:** P2

---

### Task 3.2: Find Command
**Description:** Implement `codebrain find <path> <query>` for searching.

**Acceptance Criteria:**
- Search in file paths (substring match)
- Search in symbol names
- Search in file contents (optional, grep-like)
- Return matching results with context

**Priority:** P2

---

### Task 3.3: Explain Command (Placeholder)
**Description:** Implement basic `codebrain explain <path> <target>`.

**Acceptance Criteria:**
- Shows file info from database
- Shows symbols in the file
- Shows direct dependencies and dependents
- LLM integration deferred

**Priority:** P2

---

## Priority 4: Polish & Tests

### Task 4.1: Test Coverage
**Description:** Add tests for all core functions.

**Acceptance Criteria:**
- test_scanner.py: scan_repository
- test_languages.py: detect_languages
- test_entrypoints.py: detect_entrypoints
- test_db_schema.py: schema creation
- test_cli.py: all commands

**Priority:** P1

---

### Task 4.2: Error Handling
**Description:** Add proper error handling throughout.

**Acceptance Criteria:**
- Graceful handling of missing paths
- Graceful handling of permission errors
- Informative error messages
- Non-zero exit codes on failure

**Priority:** P2

---

### Task 4.3: Logging
**Description:** Add structured logging for debugging.

**Acceptance Criteria:**
- Configurable log levels
- Logs to stderr or file
- Progress indicators for long operations

**Priority:** P3

---

## Future Tasks (Post-MVP)

- [ ] Tree-sitter integration for better parsing
- [ ] LLM integration for summaries
- [ ] Vector embeddings for semantic search
- [ ] Web UI for visualization
- [ ] GitHub integration
- [ ] Incremental analysis (watch mode)
- [ ] Cross-repository analysis
- [ ] Runtime tracing integration
