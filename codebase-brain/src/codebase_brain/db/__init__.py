"""Database layer for codebase-brain."""

from .connection import create_connection, get_db_path
from .schema import create_tables, SCHEMA_VERSION, SCHEMA_DDL

__all__ = [
    "create_connection",
    "get_db_path",
    "create_tables",
    "SCHEMA_VERSION",
    "SCHEMA_DDL",
]
