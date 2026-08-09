"""SQLite database schema definition."""

import sqlite3
from pathlib import Path


SCHEMA_VERSION = 1


SCHEMA_DDL = """
-- Schema version tracking
CREATE TABLE IF NOT EXISTS schema_info (
    version INTEGER PRIMARY KEY,
    applied_at TEXT DEFAULT (datetime('now'))
);

-- Repositories table
CREATE TABLE IF NOT EXISTS repos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    path TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    analyzed_at TEXT DEFAULT (datetime('now')),
    created_at TEXT DEFAULT (datetime('now'))
);

-- Files table
CREATE TABLE IF NOT EXISTS files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    repo_id INTEGER NOT NULL,
    path TEXT NOT NULL,
    language TEXT,
    size_bytes INTEGER,
    module_guess TEXT,
    hash TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (repo_id) REFERENCES repos(id) ON DELETE CASCADE,
    UNIQUE(repo_id, path)
);

-- Symbols table (functions, classes, variables)
CREATE TABLE IF NOT EXISTS symbols (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    kind TEXT NOT NULL CHECK(kind IN ('function', 'class', 'variable', 'constant', 'type', 'interface', 'method')),
    start_line INTEGER,
    end_line INTEGER,
    signature TEXT,
    docstring TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (file_id) REFERENCES files(id) ON DELETE CASCADE
);

-- Edges table (dependencies, imports, calls)
CREATE TABLE IF NOT EXISTS edges (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    repo_id INTEGER NOT NULL,
    source_type TEXT NOT NULL CHECK(source_type IN ('file', 'symbol')),
    source_id INTEGER NOT NULL,
    target_type TEXT NOT NULL CHECK(target_type IN ('file', 'symbol')),
    target_id INTEGER NOT NULL,
    relation TEXT NOT NULL CHECK(relation IN ('imports', 'depends_on', 'calls', 'extends', 'implements', 'contains')),
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (repo_id) REFERENCES repos(id) ON DELETE CASCADE
);

-- Summaries table (LLM-generated or computed summaries)
CREATE TABLE IF NOT EXISTS summaries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    repo_id INTEGER NOT NULL,
    target_type TEXT NOT NULL CHECK(target_type IN ('repo', 'file', 'symbol', 'module')),
    target_id INTEGER NOT NULL,
    summary TEXT NOT NULL,
    confidence REAL DEFAULT 0.5,
    evidence TEXT,
    model TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (repo_id) REFERENCES repos(id) ON DELETE CASCADE
);

-- Metadata table (key-value pairs for additional info)
CREATE TABLE IF NOT EXISTS metadata (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    repo_id INTEGER NOT NULL,
    key TEXT NOT NULL,
    value TEXT NOT NULL,
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (repo_id) REFERENCES repos(id) ON DELETE CASCADE,
    UNIQUE(repo_id, key)
);

-- Indexes for common queries
CREATE INDEX IF NOT EXISTS idx_files_repo_id ON files(repo_id);
CREATE INDEX IF NOT EXISTS idx_files_path ON files(path);
CREATE INDEX IF NOT EXISTS idx_files_language ON files(language);
CREATE INDEX IF NOT EXISTS idx_symbols_file_id ON symbols(file_id);
CREATE INDEX IF NOT EXISTS idx_symbols_name ON symbols(name);
CREATE INDEX IF NOT EXISTS idx_edges_repo_id ON edges(repo_id);
CREATE INDEX IF NOT EXISTS idx_edges_source ON edges(source_type, source_id);
CREATE INDEX IF NOT EXISTS idx_edges_target ON edges(target_type, target_id);
CREATE INDEX IF NOT EXISTS idx_summaries_repo_id ON summaries(repo_id);
CREATE INDEX IF NOT EXISTS idx_summaries_target ON summaries(target_type, target_id);
CREATE INDEX IF NOT EXISTS idx_metadata_repo_id ON metadata(repo_id);
CREATE INDEX IF NOT EXISTS idx_metadata_key ON metadata(key);
"""


def create_tables(conn: sqlite3.Connection) -> None:
    """
    Create all database tables and indexes.
    
    Args:
        conn: SQLite connection
        
    This function is idempotent - safe to call multiple times.
    Uses CREATE TABLE IF NOT EXISTS for all tables.
    """
    conn.executescript(SCHEMA_DDL)
    
    # Record schema version
    conn.execute(
        "INSERT OR IGNORE INTO schema_info (version) VALUES (?)",
        (SCHEMA_VERSION,)
    )
    conn.commit()


def get_schema_version(conn: sqlite3.Connection) -> int:
    """
    Get the current schema version from the database.
    
    Args:
        conn: SQLite connection
        
    Returns:
        Schema version number, or 0 if not found
    """
    cursor = conn.execute("SELECT version FROM schema_info ORDER BY version DESC LIMIT 1")
    row = cursor.fetchone()
    return row["version"] if row else 0


def needs_migration(conn: sqlite3.Connection) -> bool:
    """
    Check if the database needs migration.
    
    Args:
        conn: SQLite connection
        
    Returns:
        True if current schema version < SCHEMA_VERSION
    """
    current = get_schema_version(conn)
    return current < SCHEMA_VERSION


def init_database(db_path: Path) -> sqlite3.Connection:
    """
    Initialize a new database at the given path.
    
    Args:
        db_path: Path where database should be created
        
    Returns:
        SQLite connection to the new database
    """
    import sqlite3
    
    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    
    create_tables(conn)
    
    return conn
