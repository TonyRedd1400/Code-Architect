"""Tests for database connections and schema."""

import sqlite3

from codebase_brain.db.connection import create_connection, get_db_path
from codebase_brain.db.schema import (
    SCHEMA_VERSION,
    create_tables,
    get_schema_version,
    init_database,
)


def test_create_tables_and_indexes(tmp_path):
    conn = sqlite3.connect(tmp_path / "schema.db")
    try:
        create_tables(conn)
        tables = {
            row[0]
            for row in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()
        }
        indexes = {
            row[0]
            for row in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='index'"
            ).fetchall()
        }
    finally:
        conn.close()

    assert {
        "schema_info",
        "repos",
        "files",
        "symbols",
        "edges",
        "summaries",
        "metadata",
    }.issubset(tables)
    assert any(name.startswith("idx_files") for name in indexes)
    assert any(name.startswith("idx_symbols") for name in indexes)
    assert any(name.startswith("idx_edges") for name in indexes)


def test_schema_version_supports_default_row_factory():
    conn = sqlite3.connect(":memory:")
    try:
        create_tables(conn)
        assert get_schema_version(conn) == SCHEMA_VERSION
    finally:
        conn.close()


def test_schema_version_supports_row_objects():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    try:
        create_tables(conn)
        assert get_schema_version(conn) == SCHEMA_VERSION
    finally:
        conn.close()


def test_create_tables_is_idempotent():
    conn = sqlite3.connect(":memory:")
    try:
        create_tables(conn)
        create_tables(conn)
        assert get_schema_version(conn) == SCHEMA_VERSION
    finally:
        conn.close()


def test_init_database_enables_foreign_keys(tmp_path):
    conn = init_database(tmp_path / "initialized.db")
    try:
        assert conn.execute("PRAGMA foreign_keys").fetchone()[0] == 1
        assert get_schema_version(conn) == SCHEMA_VERSION
    finally:
        conn.close()


def test_create_connection_creates_parent_directory(tmp_path):
    db_path = tmp_path / "nested" / "analysis.db"
    conn = create_connection(db_path)
    conn.close()
    assert db_path.exists()


def test_default_database_path_is_outside_repository(tmp_path):
    repo_path = tmp_path / "repo"
    cache_path = tmp_path / "cache"
    repo_path.mkdir()

    db_path = get_db_path(repo_path, cache_dir=cache_path)

    assert db_path.parent == cache_path.resolve()
    assert repo_path.resolve() not in db_path.parents
    assert db_path.suffix == ".db"


def test_explicit_database_path_takes_precedence(tmp_path):
    explicit_path = tmp_path / "custom" / "brain.db"
    assert get_db_path(tmp_path, db_path=explicit_path) == explicit_path.resolve()
