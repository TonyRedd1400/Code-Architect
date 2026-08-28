"""SQLite database connection management."""

import hashlib
import os
import sqlite3
from pathlib import Path
from contextlib import contextmanager


DB_DIRECTORY = "codebase-brain"


def get_cache_dir() -> Path:
    """Return the platform-appropriate cache directory for codebase-brain."""
    if os.name == "nt":
        cache_root = os.environ.get("LOCALAPPDATA")
        if cache_root:
            return Path(cache_root) / DB_DIRECTORY

    cache_root = os.environ.get("XDG_CACHE_HOME")
    if cache_root:
        return Path(cache_root) / DB_DIRECTORY

    return Path.home() / ".cache" / DB_DIRECTORY


def get_db_path(
    repo_path: Path | str,
    db_path: Path | str | None = None,
    cache_dir: Path | str | None = None,
) -> Path:
    """
    Get the path to the SQLite database file for a repository.
    
    By default the database is stored in the user's cache directory, keeping
    analysis read-only with respect to the target repository. An explicit
    ``db_path`` always takes precedence.
    
    Args:
        repo_path: Path to the repository root
        db_path: Optional explicit database path
        cache_dir: Optional cache directory override
        
    Returns:
        Path to the database file
    """
    if db_path is not None:
        return Path(db_path).expanduser().resolve()

    resolved_repo = Path(repo_path).expanduser().resolve()
    repo_hash = hashlib.sha256(str(resolved_repo).encode("utf-8")).hexdigest()[:12]
    safe_name = "".join(
        character if character.isalnum() or character in "-_" else "-"
        for character in resolved_repo.name
    ).strip("-") or "repository"
    base_dir = Path(cache_dir).expanduser() if cache_dir else get_cache_dir()
    return base_dir.resolve() / f"{safe_name}-{repo_hash}.db"


def create_connection(db_path: Path) -> sqlite3.Connection:
    """
    Create a SQLite database connection.
    
    Args:
        db_path: Path to the database file
        
    Returns:
        SQLite connection with foreign keys enabled
    """
    db_path = Path(db_path).expanduser().resolve()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn


@contextmanager
def open_db(repo_path: Path | str, db_path: Path | str | None = None):
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
    resolved_db_path = get_db_path(repo_path, db_path=db_path)
    conn = create_connection(resolved_db_path)
    try:
        yield conn
    finally:
        conn.close()


def database_exists(repo_path: Path | str, db_path: Path | str | None = None) -> bool:
    """
    Check if a database exists for a repository.
    
    Args:
        repo_path: Path to the repository root
        
    Returns:
        True if database file exists
    """
    return get_db_path(repo_path, db_path=db_path).exists()
