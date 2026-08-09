# Architecture - codebase-brain

## Overview

codebase-brain follows a modular architecture designed for incremental development. The system is organized into layers that separate concerns: CLI interface, data ingestion, storage, analysis, and future AI integration.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         CLI Layer                            │
│                     (cli.py, commands)                       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Analysis Layer                            │
│            (overview.py, impact.py, queries.py)              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Graph Layer                             │
│            (models.py, builder.py, queries.py)               │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Ingestion Layer                            │
│        (scanner.py, languages.py, entrypoints.py)            │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Database Layer                            │
│           (schema.py, connection.py, sqlite3)                │
└─────────────────────────────────────────────────────────────┘
```

## Components

### 1. CLI Layer (`cli.py`)

**Responsibility:** User interface, command parsing, argument validation.

- Uses `argparse` for subcommand registration
- Delegates to analysis/ingestion modules
- Handles errors and exit codes
- Provides help text and documentation

**Subcommands:**
- `analyze`: Full repository scan and indexing
- `overview`: High-level summary
- `explain`: Detailed file/module explanation
- `impact`: Dependency impact analysis
- `find`: Search functionality

---

### 2. Ingestion Layer (`ingestion/`)

**Responsibility:** Extract information from source code repositories.

#### Modules:

**scanner.py**
- `scan_repository(path)` - Walk directory tree, collect files
- Handles ignore patterns (node_modules, .git, etc.)
- Returns structured file list

**languages.py**
- `detect_languages(path)` - Identify programming languages
- Extension-based detection
- Content-based hints (shebang, import statements)

**entrypoints.py**
- `detect_entrypoints(path)` - Find entry points
- package.json main field
- setup.py, __main__.py
- pom.xml, Cargo.toml, etc.

**metadata.py**
- `detect_metadata(path)` - Extract project metadata
- package.json parsing
- pyproject.toml parsing
- README detection

---

### 3. Database Layer (`db/`)

**Responsibility:** Persistent storage of extracted knowledge.

#### Tables:

**repos**
- id (PK)
- path
- name
- analyzed_at

**files**
- id (PK)
- repo_id (FK)
- path
- language
- size_bytes
- module_guess

**symbols**
- id (PK)
- file_id (FK)
- name
- kind (function/class/variable)
- start_line
- end_line

**edges**
- id (PK)
- repo_id (FK)
- source_type (file/symbol)
- source_id
- target_type (file/symbol)
- target_id
- relation (imports/depends_on/calls)

**summaries**
- id (PK)
- repo_id (FK)
- target_type
- target_id
- summary
- confidence
- evidence
- created_at

**metadata**
- id (PK)
- repo_id (FK)
- key
- value

#### Modules:

**schema.py**
- SQL DDL statements
- `create_tables(conn)` function
- Schema versioning

**connection.py**
- SQLite connection management
- Context managers
- Path resolution for DB file

---

### 4. Graph Layer (`graph/`)

**Responsibility:** Build and query dependency graphs.

#### Modules:

**models.py**
- Node classes (FileNode, SymbolNode)
- Edge classes (ImportEdge, CallEdge)
- Graph data structures

**builder.py**
- `build_graph(repo_path)` - Construct graph from indexed data
- Import statement parsing (regex-based for MVP)
- Populates edges table

**queries.py**
- `query_dependents(target)` - What depends on this?
- `query_dependencies(target)` - What does this depend on?
- Graph traversal utilities

---

### 5. Analysis Layer (`analysis/`)

**Responsibility:** High-level analysis and insights.

#### Modules:

**overview.py**
- Repository statistics
- Language breakdown
- Directory structure summary
- Entrypoint listing

**impact.py**
- Impact analysis algorithms
- Transitive dependency calculation
- Risk assessment (future)

---

### 6. LLM Layer (`llm/`) - FUTURE

**Responsibility:** Integration with language models for explanations and summaries.

**Note:** This layer is intentionally empty in MVP. Placeholder for future integration.

#### Planned Modules:

**prompts.py**
- Prompt templates for different tasks
- Context formatting utilities
- System prompts for code understanding

**summaries.py**
- `generate_summary(target)` - LLM-based summarization
- Caching strategies
- Confidence scoring

**Integration Points:**
- Will call external LLM APIs (OpenAI, Anthropic, local models)
- Will use database context for grounding
- Will store results in summaries table

---

### 7. Utilities (`utils/`)

**Responsibility:** Common helper functions.

#### Modules:

**fs.py**
- File system operations
- Safe file reading
- Hash computation

**paths.py**
- Path normalization
- Relative path handling
- Git-aware path resolution

**logging.py**
- Logger configuration
- Progress reporting
- Debug output control

---

## Data Flow

### Analyze Command Flow

```
1. CLI receives: codebrain analyze /path/to/repo
       │
       ▼
2. scanner.scan_repository() walks directory
       │
       ▼
3. languages.detect_languages() identifies langs
       │
       ▼
4. entrypoints.detect_entrypoints() finds entry points
       │
       ▼
5. db.connection.create_db() creates SQLite DB
       │
       ▼
6. db.schema.create_tables() initializes schema
       │
       ▼
7. Files inserted into files table
       │
       ▼
8. graph.builder.build_graph() extracts imports
       │
       ▼
9. Edges inserted into edges table
       │
       ▼
10. Metadata stored in metadata table
```

### Query Command Flow

```
1. CLI receives: codebrain impact /path/to/repo ./src/app.js
       │
       ▼
2. Load database from repo path
       │
       ▼
3. graph.queries.query_dependents("app.js")
       │
       ▼
4. SQL query on edges table (reverse lookup)
       │
       ▼
5. Join with files table for full paths
       │
       ▼
6. Return formatted results to CLI
```

---

## Future Integration Points

### Tree-sitter Integration

The architecture allows swapping regex-based parsing with tree-sitter:

```python
# Current (MVP)
from analysis import extract_symbols_regex

# Future
from parsers.treesitter import extract_symbols_ts
```

Planned abstraction in `parsers/` directory (not in MVP).

### LLM Integration

The `llm/` layer is prepared for future integration:

```python
# Current (MVP)
def explain_file(path):
    return "TODO: implement with LLM"

# Future
from llm.summaries import generate_summary
def explain_file(path):
    context = get_file_context(path)
    return generate_summary(context, prompt="explain")
```

### Vector Database Integration

Future enhancement for semantic search:

```
SQLite (structured) ──┬──> Hybrid Query ──> Results
                      │
Vector DB (embeddings)┘
```

---

## Design Principles

1. **Incremental Development:** Each layer can be developed independently
2. **Testability:** Pure functions where possible, dependency injection
3. **No External Dependencies:** SQLite stdlib, no network calls in MVP
4. **Read-Only Analysis:** Never modifies target repositories
5. **Local-First:** All data stored locally, no cloud dependencies
6. **Extensibility:** Clear interfaces for adding parsers, LLMs, exporters

---

## Technology Choices

| Component | Technology | Rationale |
|-----------|------------|-----------|
| Language | Python 3.11+ | Rich ecosystem, easy prototyping |
| CLI | argparse | Standard library, no dependencies |
| Database | SQLite | Embedded, no server, standard library |
| Testing | pytest | Industry standard, fixtures |
| Parsing (MVP) | Regex | Simple, no dependencies |
| Parsing (Future) | Tree-sitter | Fast, accurate, multi-language |
| LLM (Future) | API calls | Flexible provider choice |

---

## Module Dependencies

```
cli → analysis → graph → db
cli → ingestion → db
utils → (used by all)
llm → analysis (future)
```

No circular dependencies allowed.
