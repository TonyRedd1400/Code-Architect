"""Repository overview generation."""

from pathlib import Path
from typing import Any
from collections import defaultdict


def get_overview(repo_path: Path | str) -> dict[str, Any]:
    """
    Generate a high-level overview of a repository.
    
    This is a placeholder/stub for the MVP. Future implementation will
    provide detailed statistics about files, languages, structure, etc.
    
    Args:
        repo_path: Path to the repository root
        
    Returns:
        Dictionary with overview information:
        {
            "path": "...",
            "name": "...",
            "total_files": 0,
            "languages": {},
            "directories": [],
            "entrypoints": [],
            "metadata": {},
        }
        
    Example:
        overview = get_overview("/path/to/repo")
        print(f"Files: {overview['total_files']}")
        print(f"Languages: {overview['languages']}")
    """
    if isinstance(repo_path, str):
        repo_path = Path(repo_path)
    
    repo_path = repo_path.resolve()
    
    # TODO: Implement full overview generation
    # For now, return minimal placeholder
    
    return {
        "path": str(repo_path),
        "name": repo_path.name,
        "total_files": 0,
        "total_size_bytes": 0,
        "languages": {},
        "directories": [],
        "entrypoints": [],
        "metadata": {},
        "note": "TODO: implement full overview",
    }


def format_overview_text(overview: dict[str, Any]) -> str:
    """
    Format overview as human-readable text.
    
    Args:
        overview: Overview dictionary from get_overview()
        
    Returns:
        Formatted text string
    """
    lines = [
        f"Repository: {overview.get('name', 'unknown')}",
        f"Path: {overview.get('path', '')}",
        "",
        f"Total files: {overview.get('total_files', 0)}",
        f"Total size: {overview.get('total_size_bytes', 0)} bytes",
        "",
        "Languages:",
    ]
    
    languages = overview.get("languages", {})
    if languages:
        for lang, count in sorted(languages.items(), key=lambda x: -x[1]):
            lines.append(f"  {lang}: {count}")
    else:
        lines.append("  (none detected)")
    
    lines.append("")
    lines.append("Entrypoints:")
    entrypoints = overview.get("entrypoints", [])
    if entrypoints:
        for ep in entrypoints:
            lines.append(f"  - {ep.get('path', '')} ({ep.get('ecosystem', '')})")
    else:
        lines.append("  (none detected)")
    
    return "\n".join(lines)
