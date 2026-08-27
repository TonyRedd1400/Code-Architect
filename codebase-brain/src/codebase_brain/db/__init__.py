"""Database layer for codebase-brain."""

from .connection import create_connection, get_cache_dir, get_db_path, open_db
from .schema import create_tables, init_database, SCHEMA_VERSION, SCHEMA_DDL

__all__ = [
    "create_connection",
    "get_cache_dir",
    "get_db_path",
    "open_db",
    "create_tables",
    "init_database",
    "SCHEMA_VERSION",
    "SCHEMA_DDL",
]
