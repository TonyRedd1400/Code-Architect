"""Configuration management for codebase-brain."""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class Config:
    """Application configuration."""
    
    # Database settings
    db_filename: str = ".codebrain.db"
    
    # Ignore patterns for scanning
    ignore_dirs: tuple[str, ...] = (
        "node_modules",
        "dist",
        "build",
        ".git",
        "coverage",
        "__pycache__",
        ".venv",
        "venv",
        "vendor",
        "target",  # Rust
        ".idea",
        ".vscode",
    )
    
    ignore_files: tuple[str, ...] = (
        ".DS_Store",
        "Thumbs.db",
    )
    
    ignore_extensions: tuple[str, ...] = (
        ".pyc",
        ".pyo",
        ".so",
        ".dll",
        ".exe",
        ".bin",
    )
    
    # Max file size to process (in bytes)
    max_file_size: int = 10 * 1024 * 1024  # 10 MB
    
    # Supported languages (by extension)
    language_extensions: dict[str, str] = None  # Initialized in __post_init__
    
    def __post_init__(self):
        if self.language_extensions is None:
            self.language_extensions = {
                ".py": "python",
                ".js": "javascript",
                ".jsx": "javascript",
                ".ts": "typescript",
                ".tsx": "typescript",
                ".java": "java",
                ".go": "go",
                ".rs": "rust",
                ".rb": "ruby",
                ".php": "php",
                ".cpp": "cpp",
                ".cc": "cpp",
                ".cxx": "cpp",
                ".h": "cpp",
                ".hpp": "cpp",
                ".cs": "csharp",
                ".swift": "swift",
                ".kt": "kotlin",
                ".scala": "scala",
                ".r": "r",
                ".R": "r",
                ".sql": "sql",
                ".sh": "shell",
                ".bash": "shell",
                ".zsh": "shell",
                ".yaml": "yaml",
                ".yml": "yaml",
                ".json": "json",
                ".xml": "xml",
                ".html": "html",
                ".css": "css",
                ".scss": "scss",
                ".md": "markdown",
                ".toml": "toml",
                ".ini": "ini",
                ".cfg": "ini",
                ".lua": "lua",
                ".ex": "elixir",
                ".exs": "elixir",
                ".erl": "erlang",
                ".hs": "haskell",
                ".clj": "clojure",
                ".vue": "vue",
                ".svelte": "svelte",
            }


# Global default config instance
default_config = Config()


def get_config() -> Config:
    """Get the current configuration."""
    return default_config
