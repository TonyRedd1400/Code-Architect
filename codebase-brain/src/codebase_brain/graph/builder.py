"""Graph builder - constructs dependency graph from repository."""

import re
from pathlib import Path
from typing import Any

from .models import FileNode, SymbolNode, Edge, DependencyGraph
from ..ingestion import scan_repository


def build_graph(repo_path: Path | str) -> DependencyGraph:
    """
    Build a dependency graph from a repository.
    
    This is a placeholder/stub implementation for the MVP.
    It creates a basic graph structure with files but minimal edges.
    
    TODO: Implement proper import parsing for:
    - Python: import x, from x import y
    - JavaScript: import ..., require(...)
    - Other languages as needed
    
    Args:
        repo_path: Path to the repository root
        
    Returns:
        DependencyGraph with files and basic edges
        
    Example:
        graph = build_graph("/path/to/repo")
        print(f"Files: {len(graph.files)}")
        print(f"Edges: {len(graph.edges)}")
    """
    if isinstance(repo_path, str):
        repo_path = Path(repo_path)
    
    repo_path = repo_path.resolve()
    graph = DependencyGraph()
    
    # Scan repository
    scan_result = scan_repository(repo_path)
    
    # Add files to graph
    for idx, file_info in enumerate(scan_result.files):
        file_node = FileNode(
            id=idx + 1,
            path=file_info["path"],
            language=file_info.get("extension", "").lstrip("."),
            size_bytes=file_info.get("size_bytes", 0),
        )
        graph.add_file(file_node)
    
    # TODO: Extract symbols from files
    # For now, this is a stub - symbols will be added in future iteration
    # extract_symbols(graph, repo_path)
    
    # TODO: Extract import edges between files
    # For now, this is a stub - edges will be added in future iteration
    # extract_imports(graph, repo_path)
    
    return graph


def extract_symbols(graph: DependencyGraph, repo_path: Path) -> None:
    """
    Extract symbols (functions, classes) from files.
    
    TODO: Implement regex-based symbol extraction.
    
    Args:
        graph: Graph to add symbols to
        repo_path: Repository path
    """
    # Placeholder for future implementation
    pass


def extract_imports(graph: DependencyGraph, repo_path: Path) -> None:
    """
    Extract import relationships between files.
    
    TODO: Implement import parsing for different languages.
    
    Args:
        graph: Graph to add edges to
        repo_path: Repository path
    """
    # Placeholder for future implementation
    pass


# Simple regex patterns for future use (not used in MVP)
PYTHON_IMPORT_PATTERN = re.compile(
    r'^(?:import\s+(\w+)|from\s+(\w+)\s+import)',
    re.MULTILINE
)

JS_IMPORT_PATTERN = re.compile(
    r'^(?:import\s+.*?\s+from\s+[\'"](.+?)[\'"]|require\([\'"](.+?)[\'"])',
    re.MULTILINE
)

PYTHON_FUNC_PATTERN = re.compile(
    r'^\s*def\s+(\w+)\s*\(',
    re.MULTILINE
)

PYTHON_CLASS_PATTERN = re.compile(
    r'^\s*class\s+(\w+)',
    re.MULTILINE
)

JS_FUNC_PATTERN = re.compile(
    r'(?:function\s+(\w+)|(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?(?:\([^)]*\)|[^=])\s*=>)',
)

JS_CLASS_PATTERN = re.compile(
    r'class\s+(\w+)',
)
