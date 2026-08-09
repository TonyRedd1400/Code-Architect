"""Tests for database schema."""

import sqlite3
import tempfile
from pathlib import Path

from codebase_brain.db.schema import (
    create_tables,
    SCHEMA_DDL,
    SCHEMA_VERSION,
    get_schema_version,
    init_database,
)


def test_create_tables():
    """Test that tables can be created without errors."""
    with tempfile.NamedTemporaryFile(suffix=".db") as tmp:
        conn = sqlite3.connect(tmp.name)
        try:
            create_tables(conn)
            # If we get here without exception, test passes
        finally:
            conn.close()


def test_schema_version():
    """Test that schema version is recorded."""
    with tempfile.NamedTemporaryFile(suffix=".db") as tmp:
        conn = sqlite3.connect(tmp.name)
        try:
            create_tables(conn)
            version = get_schema_version(conn)
            assert version == SCHEMA_VERSION
        finally:
            conn.close()


def test_tables_exist():
    """Test that all expected tables are created."""
    with tempfile.NamedTemporaryFile(suffix=".db") as tmp:
        conn = sqlite3.connect(tmp.name)
        try:
            create_tables(conn)
            
            # Check all tables exist
            cursor = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
            )
            tables = {row[0] for row in cursor.fetchall()}
            
            expected_tables = {
                'schema_info',
                'repos',
                'files',
                'symbols',
                'edges',
                'summaries',
                'metadata',
            }
            
            assert expected_tables.issubset(tables), f"Missing tables: {expected_tables - tables}"
        finally:
            conn.close()


def test_indexes_exist():
    """Test that indexes are created."""
    with tempfile.NamedTemporaryFile(suffix=".db") as tmp:
        conn = sqlite3.connect(tmp.name)
        try:
            create_tables(conn)
            
            cursor = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='index' ORDER BY name"
            )
            indexes = {row[0] for row in cursor.fetchall()}
            
            # Check some key indexes exist
            assert any('idx_files' in idx for idx in indexes)
            assert any('idx_symbols' in idx for idx in indexes)
            assert any('idx_edges' in idx for idx in indexes)
        finally:
            conn.close()


def test_foreign_keys_enabled():
    """Test that foreign keys can be enabled."""
    with tempfile.NamedTemporaryFile(suffix=".db") as tmp:
        conn = sqlite3.connect(tmp.name)
        try:
            conn.execute("PRAGMA foreign_keys = ON")
            cursor = conn.execute("PRAGMA foreign_keys")
            result = cursor.fetchone()
            assert result[0] == 1
        finally:
            conn.close()


def test_init_database():
    """Test full database initialization."""
    with tempfile.NamedTemporaryFile(suffix=".db") as tmp:
        db_path = Path(tmp.name)
        conn = init_database(db_path)
        try:
            version = get_schema_version(conn)
            assert version == SCHEMA_VERSION
            
            # Verify we can insert data
            conn.execute(
                "INSERT INTO repos (path, name) VALUES (?, ?)",
                ("/test/repo", "test-repo")
            )
            conn.commit()
            
            cursor = conn.execute("SELECT COUNT(*) FROM repos")
            count = cursor.fetchone()[0]
            assert count == 1
        finally:
            conn.close()


def test_idempotent_table_creation():
    """Test that create_tables can be called multiple times."""
    with tempfile.NamedTemporaryFile(suffix=".db") as tmp:
        conn = sqlite3.connect(tmp.name)
        try:
            # Call multiple times
            create_tables(conn)
            create_tables(conn)
            create_tables(conn)
            
            # Should still work
            version = get_schema_version(conn)
            assert version == SCHEMA_VERSION
        finally:
            conn.close()
