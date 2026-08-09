"""SQLite database connection management."""

import sqlite3
from pathlib import Path
from contextlib import contextmanager


DB_FILENAME = ".codebrain.db"


def get_db_path(repo_path: Path) -> Path:
    """
    Get the path to the SQLite database file for a repository.
    
    The database is stored in the root of the repository as .codebrain.db
    
    Args:
        repo_path: Path to the repository root
        
    Returns:
        Path to the database file
    """
    return repo_path / DB_FILENAME


def create_connection(db_path: Path) -> sqlite3.Connection:
    """
    Create a SQLite database connection.
    
    Args:
        db_path: Path to the database file
        
    Returns:
        SQLite connection with foreign keys enabled
    """
    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn


@contextmanager
def open_db(repo_path: Path):
    """
    Context manager for database connections.
    
    Args:
        repo_path: Path to the repository root
        
    Yields:
        SQLite connection
        
    Example:
        with open_db(repo_path) as conn:
            cursor = conn.execute("SELECT * FROM files")
    """
    db_path = get_db_path(repo_path)
    conn = create_connection(db_path)
    try:
        yield conn
    finally:
        conn.close()


def database_exists(repo_path: Path) -> bool:
    """
    Check if a database exists for a repository.
    
    Args:
        repo_path: Path to the repository root
        
    Returns:
        True if database file exists
    """
    return get_db_path(repo_path).exists()
