"""Path utilities."""

from pathlib import Path


def normalize_path(path: Path | str, base: Path | str | None = None) -> str:
    """
    Normalize a path to a consistent string format.
    
    Args:
        path: Path to normalize
        base: Base path for relative resolution (optional)
        
    Returns:
        Normalized path string
        
    Example:
        normalize_path("./src/../lib/file.py")  # returns "lib/file.py"
    """
    if isinstance(path, str):
        path = Path(path)
    
    if base is not None:
        if isinstance(base, str):
            base = Path(base)
        path = base / path
    
    # Resolve and convert to posix-style path
    resolved = path.resolve()
    return resolved.as_posix()


def is_subpath(child: Path | str, parent: Path | str) -> bool:
    """
    Check if child path is under parent path.
    
    Args:
        child: Child path
        parent: Parent path
        
    Returns:
        True if child is a subpath of parent
        
    Example:
        is_subpath("/repo/src/app.py", "/repo")  # True
        is_subpath("/other/file.py", "/repo")    # False
    """
    if isinstance(child, str):
        child = Path(child)
    if isinstance(parent, str):
        parent = Path(parent)
    
    try:
        child.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def make_relative(path: Path | str, base: Path | str) -> str:
    """
    Make a path relative to a base path.
    
    Args:
        path: Absolute path
        base: Base path to make relative to
        
    Returns:
        Relative path string
        
    Example:
        make_relative("/repo/src/app.py", "/repo")  # returns "src/app.py"
    """
    if isinstance(path, str):
        path = Path(path)
    if isinstance(base, str):
        base = Path(base)
    
    try:
        return str(path.resolve().relative_to(base.resolve()))
    except ValueError:
        # Path is not relative to base
        return str(path)


def join_paths(*parts: str) -> str:
    """
    Join path parts safely.
    
    Args:
        *parts: Path parts to join
        
    Returns:
        Joined path string
        
    Example:
        join_paths("src", "components", "App.tsx")  # returns "src/components/App.tsx"
    """
    if not parts:
        return ""
    
    result = Path(parts[0])
    for part in parts[1:]:
        result = result / part
    
    return result.as_posix()
