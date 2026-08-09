"""Graph data models for dependency tracking."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class FileNode:
    """Represents a file in the dependency graph."""
    
    id: int
    path: str
    language: str | None = None
    size_bytes: int = 0
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "path": self.path,
            "language": self.language,
            "size_bytes": self.size_bytes,
        }


@dataclass
class SymbolNode:
    """Represents a symbol (function, class, etc.) in the graph."""
    
    id: int
    file_id: int
    name: str
    kind: str  # function, class, variable, etc.
    start_line: int | None = None
    end_line: int | None = None
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "file_id": self.file_id,
            "name": self.name,
            "kind": self.kind,
            "start_line": self.start_line,
            "end_line": self.end_line,
        }


@dataclass
class Edge:
    """Represents a relationship between two nodes."""
    
    id: int
    source_type: str  # 'file' or 'symbol'
    source_id: int
    target_type: str  # 'file' or 'symbol'
    target_id: int
    relation: str  # imports, depends_on, calls, extends, implements, contains
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "source_type": self.source_type,
            "source_id": self.source_id,
            "target_type": self.target_type,
            "target_id": self.target_id,
            "relation": self.relation,
        }


@dataclass
class DependencyGraph:
    """In-memory representation of the dependency graph."""
    
    files: list[FileNode] = field(default_factory=list)
    symbols: list[SymbolNode] = field(default_factory=list)
    edges: list[Edge] = field(default_factory=list)
    
    # Indexes for fast lookup
    _file_by_id: dict[int, FileNode] = field(default_factory=dict)
    _file_by_path: dict[str, FileNode] = field(default_factory=dict)
    _edges_from: dict[int, list[Edge]] = field(default_factory=dict)
    _edges_to: dict[int, list[Edge]] = field(default_factory=dict)
    
    def add_file(self, file: FileNode) -> None:
        """Add a file node to the graph."""
        self.files.append(file)
        self._file_by_id[file.id] = file
        self._file_by_path[file.path] = file
    
    def add_symbol(self, symbol: SymbolNode) -> None:
        """Add a symbol node to the graph."""
        self.symbols.append(symbol)
    
    def add_edge(self, edge: Edge) -> None:
        """Add an edge to the graph."""
        self.edges.append(edge)
        
        # Update indexes
        if edge.source_id not in self._edges_from:
            self._edges_from[edge.source_id] = []
        self._edges_from[edge.source_id].append(edge)
        
        if edge.target_id not in self._edges_to:
            self._edges_to[edge.target_id] = []
        self._edges_to[edge.target_id].append(edge)
    
    def get_file_by_id(self, file_id: int) -> FileNode | None:
        """Get a file by its ID."""
        return self._file_by_id.get(file_id)
    
    def get_file_by_path(self, path: str) -> FileNode | None:
        """Get a file by its path."""
        return self._file_by_path.get(path)
    
    def get_edges_from(self, node_id: int) -> list[Edge]:
        """Get all edges originating from a node."""
        return self._edges_from.get(node_id, [])
    
    def get_edges_to(self, node_id: int) -> list[Edge]:
        """Get all edges pointing to a node."""
        return self._edges_to.get(node_id, [])
    
    def get_dependents(self, node_id: int) -> list[Edge]:
        """
        Get all nodes that depend on this node.
        
        Args:
            node_id: ID of the node
            
        Returns:
            List of edges where this node is the target
        """
        return self.get_edges_to(node_id)
    
    def get_dependencies(self, node_id: int) -> list[Edge]:
        """
        Get all nodes that this node depends on.
        
        Args:
            node_id: ID of the node
            
        Returns:
            List of edges where this node is the source
        """
        return self.get_edges_from(node_id)
    
    def to_dict(self) -> dict[str, Any]:
        """Convert graph to dictionary."""
        return {
            "files": [f.to_dict() for f in self.files],
            "symbols": [s.to_dict() for s in self.symbols],
            "edges": [e.to_dict() for e in self.edges],
            "statistics": {
                "file_count": len(self.files),
                "symbol_count": len(self.symbols),
                "edge_count": len(self.edges),
            }
        }
