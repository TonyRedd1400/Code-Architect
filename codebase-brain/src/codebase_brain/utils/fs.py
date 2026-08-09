"""File system utilities."""

import hashlib
from pathlib import Path
from typing import Any


def read_file_safe(file_path: Path | str, max_size: int = 10 * 1024 * 1024) -> str | None:
    """
    Safely read a file with size limits and error handling.
    
    Args:
        file_path: Path to the file
        max_size: Maximum file size to read (default 10MB)
        
    Returns:
        File contents as string, or None if file can't be read
        
    Example:
        content = read_file_safe("src/app.py")
        if content:
            print(f"Read {len(content)} characters")
    """
    if isinstance(file_path, str):
        file_path = Path(file_path)
    
    try:
        # Check file size first
        stat_info = file_path.stat()
        if stat_info.st_size > max_size:
            return None
        
        # Read file
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
            
    except (OSError, PermissionError, UnicodeDecodeError):
        return None


def file_hash(file_path: Path | str, algorithm: str = "sha256") -> str | None:
    """
    Compute hash of a file.
    
    Args:
        file_path: Path to the file
        algorithm: Hash algorithm (default sha256)
        
    Returns:
        Hex digest of file hash, or None if file can't be read
        
    Example:
        h = file_hash("src/app.py")
        print(f"SHA256: {h}")
    """
    if isinstance(file_path, str):
        file_path = Path(file_path)
    
    try:
        hasher = hashlib.new(algorithm)
        
        with open(file_path, "rb") as f:
            # Read in chunks for large files
            while chunk := f.read(8192):
                hasher.update(chunk)
        
        return hasher.hexdigest()
        
    except (OSError, PermissionError):
        return None


def get_file_size(file_path: Path | str) -> int | None:
    """
    Get file size in bytes.
    
    Args:
        file_path: Path to the file
        
    Returns:
        File size in bytes, or None if file doesn't exist
    """
    if isinstance(file_path, str):
        file_path = Path(file_path)
    
    try:
        return file_path.stat().st_size
    except OSError:
        return None


def count_lines(file_path: Path | str) -> int:
    """
    Count lines in a file.
    
    Args:
        file_path: Path to the file
        
    Returns:
        Number of lines, or 0 if file can't be read
    """
    if isinstance(file_path, str):
        file_path = Path(file_path)
    
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return sum(1 for _ in f)
    except (OSError, PermissionError):
        return 0
