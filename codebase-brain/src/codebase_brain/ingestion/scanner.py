"""Repository scanner - walks directory tree and collects file information."""

import os
from pathlib import Path
from typing import Any
from dataclasses import dataclass, field

from ..config import get_config


@dataclass
class ScanResult:
    """Result of repository scanning."""
    
    path: str
    files: list[dict[str, Any]] = field(default_factory=list)
    total_files: int = 0
    total_size_bytes: int = 0
    directories_scanned: int = 0
    directories_ignored: int = 0
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "path": self.path,
            "files": self.files,
            "total_files": self.total_files,
            "total_size_bytes": self.total_size_bytes,
            "directories_scanned": self.directories_scanned,
            "directories_ignored": self.directories_ignored,
        }


def should_ignore_dir(dir_name: str, config=None) -> bool:
    """
    Check if a directory should be ignored.
    
    Args:
        dir_name: Directory name (not full path)
        config: Configuration object
        
    Returns:
        True if directory should be skipped
    """
    if config is None:
        config = get_config()
    
    return dir_name in config.ignore_dirs or dir_name.startswith(".")


def should_ignore_file(file_name: str, config=None) -> bool:
    """
    Check if a file should be ignored.
    
    Args:
        file_name: File name (not full path)
        config: Configuration object
        
    Returns:
        True if file should be skipped
    """
    if config is None:
        config = get_config()
    
    # Check exact filename matches
    if file_name in config.ignore_files:
        return True
    
    # Check extension matches
    suffix = Path(file_name).suffix.lower()
    if suffix in config.ignore_extensions:
        return True
    
    return False


def scan_repository(repo_path: Path | str) -> ScanResult:
    """
    Scan a repository and collect file information.
    
    Walks the directory tree, ignoring common directories like node_modules,
    .git, dist, etc. Collects information about each file.
    
    Args:
        repo_path: Path to the repository root
        
    Returns:
        ScanResult with file list and statistics
        
    Example:
        result = scan_repository("/path/to/repo")
        for file_info in result.files:
            print(f"{file_info['path']} ({file_info['size_bytes']} bytes)")
    """
    if isinstance(repo_path, str):
        repo_path = Path(repo_path)
    
    repo_path = repo_path.resolve()
    config = get_config()
    
    result = ScanResult(path=str(repo_path))
    
    if not repo_path.exists():
        raise FileNotFoundError(f"Repository path does not exist: {repo_path}")
    
    if not repo_path.is_dir():
        raise NotADirectoryError(f"Repository path is not a directory: {repo_path}")
    
    # Walk the directory tree
    for root, dirs, files in os.walk(repo_path):
        root_path = Path(root)
        
        # Filter out ignored directories (modifies dirs in-place)
        original_dir_count = len(dirs)
        dirs[:] = [d for d in dirs if not should_ignore_dir(d, config)]
        result.directories_ignored += original_dir_count - len(dirs)
        result.directories_scanned += len(dirs)
        
        # Process files
        for file_name in files:
            if should_ignore_file(file_name, config):
                continue
            
            file_path = root_path / file_name
            
            try:
                stat_info = file_path.stat()
                size_bytes = stat_info.st_size
                
                # Skip files that are too large
                if size_bytes > config.max_file_size:
                    continue
                
                relative_path = str(file_path.relative_to(repo_path))
                suffix = file_path.suffix.lower()
                
                file_info = {
                    "path": relative_path,
                    "absolute_path": str(file_path),
                    "extension": suffix,
                    "size_bytes": size_bytes,
                    "name": file_name,
                    "directory": str(file_path.parent.relative_to(repo_path)),
                }
                
                result.files.append(file_info)
                result.total_files += 1
                result.total_size_bytes += size_bytes
                
            except (OSError, PermissionError):
                # Skip files we can't access
                continue
    
    return result


def scan_repository_minimal(repo_path: Path | str) -> dict[str, Any]:
    """
    Minimal scan returning just basic structure.
    
    This is a simpler version for quick checks.
    
    Args:
        repo_path: Path to the repository root
        
    Returns:
        Dictionary with path, files list, and basic counts
    """
    result = scan_repository(repo_path)
    return {
        "path": result.path,
        "files": [f["path"] for f in result.files],
        "total_files": result.total_files,
        "total_size_bytes": result.total_size_bytes,
    }
