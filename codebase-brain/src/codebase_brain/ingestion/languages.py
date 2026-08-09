"""Language detection for source files."""

from pathlib import Path
from typing import Any
from collections import defaultdict

from ..config import get_config


def get_language_from_extension(extension: str, config=None) -> str | None:
    """
    Get language name from file extension.
    
    Args:
        extension: File extension (e.g., '.py', '.js')
        config: Configuration object
        
    Returns:
        Language name or None if not recognized
        
    Example:
        get_language_from_extension('.py')  # returns 'python'
        get_language_from_extension('.js')  # returns 'javascript'
    """
    if config is None:
        config = get_config()
    
    return config.language_extensions.get(extension.lower())


def detect_languages(repo_path: Path | str) -> dict[str, Any]:
    """
    Detect programming languages in a repository.
    
    Scans all files and counts occurrences by language based on
    file extensions.
    
    Args:
        repo_path: Path to the repository root
        
    Returns:
        Dictionary with language statistics:
        {
            "languages": {"python": 10, "javascript": 5, ...},
            "total_files": 15,
            "by_extension": {".py": 10, ".js": 5, ...},
            "primary_language": "python",
        }
        
    Example:
        result = detect_languages("/path/to/repo")
        print(f"Primary language: {result['primary_language']}")
        print(f"Languages found: {list(result['languages'].keys())}")
    """
    from .scanner import scan_repository
    
    if isinstance(repo_path, str):
        repo_path = Path(repo_path)
    
    repo_path = repo_path.resolve()
    config = get_config()
    
    # Scan the repository
    scan_result = scan_repository(repo_path)
    
    language_counts: dict[str, int] = defaultdict(int)
    extension_counts: dict[str, int] = defaultdict(int)
    total_counted = 0
    
    for file_info in scan_result.files:
        ext = file_info["extension"]
        
        # Count by extension
        if ext:
            extension_counts[ext] += 1
        
        # Count by language
        language = get_language_from_extension(ext, config)
        if language:
            language_counts[language] += 1
            total_counted += 1
    
    # Determine primary language
    primary_language = None
    if language_counts:
        primary_language = max(language_counts.keys(), key=lambda k: language_counts[k])
    
    return {
        "path": str(repo_path),
        "languages": dict(language_counts),
        "total_files": scan_result.total_files,
        "files_with_recognized_language": total_counted,
        "by_extension": dict(extension_counts),
        "primary_language": primary_language,
    }


def detect_language_by_content(file_path: Path) -> str | None:
    """
    Attempt to detect language by file content (shebang, imports).
    
    This is a fallback for files without extensions or ambiguous extensions.
    
    Args:
        file_path: Path to the file
        
    Returns:
        Detected language or None
    """
    try:
        # Read first few lines
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            first_lines = f.read(500)
        
        # Check shebang
        if first_lines.startswith("#!"):
            first_line = first_lines.split("\n")[0]
            if "python" in first_line:
                return "python"
            elif "node" in first_line or "js" in first_line:
                return "javascript"
            elif "bash" in first_line or "sh" in first_line:
                return "shell"
            elif "ruby" in first_line:
                return "ruby"
            elif "perl" in first_line:
                return "perl"
        
        # Check for language-specific patterns
        lines = first_lines.split("\n")[:10]
        for line in lines:
            line = line.strip()
            
            # Python
            if line.startswith("import ") or line.startswith("from "):
                if " def " in line or " class " in line:
                    return "python"
            
            # JavaScript/TypeScript
            if line.startswith("import ") or line.startswith("export "):
                if "{" in line or "}" in line:
                    return "typescript" if ".ts" in str(file_path) else "javascript"
            if line.startswith("const ") or line.startswith("let ") or line.startswith("var "):
                if "=" in line:
                    return "typescript" if ".ts" in str(file_path) else "javascript"
        
    except (OSError, PermissionError, UnicodeDecodeError):
        pass
    
    return None


def get_all_supported_languages() -> list[str]:
    """
    Get list of all supported languages.
    
    Returns:
        List of language names
    """
    config = get_config()
    return list(set(config.language_extensions.values()))
