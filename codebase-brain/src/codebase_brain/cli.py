"""
CLI entry point for codebase-brain.

Provides subcommands:
- analyze: Full repository analysis
- overview: High-level summary
- explain: Explain a specific file or module
- impact: Analyze impact of changes
- find: Search for files or symbols
"""

import argparse
import json
import sqlite3
import sys
from pathlib import Path

from .analysis.overview import format_overview_text, get_overview
from .db import get_db_path, init_database
from .ingestion import (
    detect_entrypoints,
    detect_languages,
    detect_metadata,
    get_language_from_extension,
    scan_repository,
)
from .utils.fs import file_hash


NOT_IMPLEMENTED_EXIT = 2


def _resolve_repository(repo_path: str) -> Path | None:
    """Resolve and validate a repository directory, printing CLI errors."""
    resolved = Path(repo_path).expanduser().resolve()
    if not resolved.exists():
        print(f"Error: Repository path does not exist: {resolved}", file=sys.stderr)
        return None
    if not resolved.is_dir():
        print(f"Error: Repository path is not a directory: {resolved}", file=sys.stderr)
        return None
    return resolved


def _persist_analysis(repo_path: Path, db_path: Path) -> dict[str, object]:
    """Scan a repository and persist its current file-level analysis."""
    scan = scan_repository(repo_path)
    languages = detect_languages(repo_path)
    entrypoints = detect_entrypoints(repo_path)
    metadata = detect_metadata(repo_path)

    conn = init_database(db_path)
    try:
        conn.execute(
            """
            INSERT INTO repos (path, name) VALUES (?, ?)
            ON CONFLICT(path) DO UPDATE SET
                name = excluded.name,
                analyzed_at = datetime('now')
            """,
            (str(repo_path), metadata.get("name", repo_path.name)),
        )
        repo_id = conn.execute(
            "SELECT id FROM repos WHERE path = ?", (str(repo_path),)
        ).fetchone()[0]

        # A new scan replaces file-derived data from the previous run.
        conn.execute("DELETE FROM edges WHERE repo_id = ?", (repo_id,))
        conn.execute("DELETE FROM summaries WHERE repo_id = ?", (repo_id,))
        conn.execute("DELETE FROM files WHERE repo_id = ?", (repo_id,))
        for file_info in scan.files:
            conn.execute(
                """
                INSERT INTO files (repo_id, path, language, size_bytes, hash)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    repo_id,
                    file_info["path"],
                    get_language_from_extension(file_info["extension"]),
                    file_info["size_bytes"],
                    file_hash(file_info["absolute_path"]),
                ),
            )

        stored_metadata = {
            **metadata,
            "languages": languages,
            "entrypoints": entrypoints,
        }
        conn.execute("DELETE FROM metadata WHERE repo_id = ?", (repo_id,))
        conn.executemany(
            "INSERT INTO metadata (repo_id, key, value) VALUES (?, ?, ?)",
            [
                (repo_id, key, json.dumps(value, ensure_ascii=False, sort_keys=True))
                for key, value in stored_metadata.items()
            ],
        )
        conn.commit()
    finally:
        conn.close()

    return {
        "database": str(db_path),
        "total_files": scan.total_files,
        "languages": languages["languages"],
        "entrypoints": entrypoints,
    }


def _not_implemented(command: str) -> int:
    print(
        f"Error: '{command}' is not implemented in this MVP.",
        file=sys.stderr,
    )
    return NOT_IMPLEMENTED_EXIT


def cmd_analyze(args: argparse.Namespace) -> int:
    """Handle the 'analyze' subcommand."""
    repo_path = _resolve_repository(args.repo_path)
    if repo_path is None:
        return 1

    db_path = get_db_path(repo_path, db_path=args.db_path)
    try:
        result = _persist_analysis(repo_path, db_path)
    except (OSError, sqlite3.Error) as exc:
        print(f"Error: Analysis failed: {exc}", file=sys.stderr)
        return 1

    print(f"Analyzed: {repo_path}")
    print(f"Files indexed: {result['total_files']}")
    print(f"Database: {result['database']}")
    return 0


def cmd_overview(args: argparse.Namespace) -> int:
    """Handle the 'overview' subcommand."""
    repo_path = _resolve_repository(args.repo_path)
    if repo_path is None:
        return 1

    try:
        print(format_overview_text(get_overview(repo_path)))
    except OSError as exc:
        print(f"Error: Overview failed: {exc}", file=sys.stderr)
        return 1
    return 0


def cmd_explain(args: argparse.Namespace) -> int:
    """Handle the 'explain' subcommand."""
    repo_path = _resolve_repository(args.repo_path)
    if repo_path is None:
        return 1
    return _not_implemented("explain")


def cmd_impact(args: argparse.Namespace) -> int:
    """Handle the 'impact' subcommand."""
    repo_path = _resolve_repository(args.repo_path)
    if repo_path is None:
        return 1
    return _not_implemented("impact")


def cmd_find(args: argparse.Namespace) -> int:
    """Handle the 'find' subcommand."""
    repo_path = _resolve_repository(args.repo_path)
    if repo_path is None:
        return 1
    return _not_implemented("find")


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        prog="codebrain",
        description="Convert code repositories into navigable knowledge bases for AI agents.",
        epilog="Use '%(prog)s <command> --help' for more information about a command.",
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0",
    )
    
    subparsers = parser.add_subparsers(
        dest="command",
        title="commands",
        description="Available commands",
    )
    
    # analyze command
    analyze_parser = subparsers.add_parser(
        "analyze",
        help="Perform full repository analysis and create knowledge base",
        description="Scan a repository, detect languages and entrypoints, "
                    "and store file-level results in a SQLite database.",
    )
    analyze_parser.add_argument(
        "repo_path",
        type=str,
        help="Path to the repository to analyze",
    )
    analyze_parser.add_argument(
        "--db-path",
        type=str,
        help="Explicit SQLite output path (default: platform user cache)",
    )
    analyze_parser.set_defaults(func=cmd_analyze)
    
    # overview command
    overview_parser = subparsers.add_parser(
        "overview",
        help="Show high-level summary of a repository",
        description="Display statistics about files, languages, directories, "
                    "and entrypoints in a repository.",
    )
    overview_parser.add_argument(
        "repo_path",
        type=str,
        help="Path to the repository",
    )
    overview_parser.set_defaults(func=cmd_overview)
    
    # explain command
    explain_parser = subparsers.add_parser(
        "explain",
        help="Explain a specific file or module",
        description="Provide detailed information about a file or module, "
                    "including symbols, dependencies, and summary.",
    )
    explain_parser.add_argument(
        "repo_path",
        type=str,
        help="Path to the repository",
    )
    explain_parser.add_argument(
        "target_path",
        type=str,
        help="Path to the file or module to explain",
    )
    explain_parser.set_defaults(func=cmd_explain)
    
    # impact command
    impact_parser = subparsers.add_parser(
        "impact",
        help="Analyze impact of changes to a target",
        description="Find what depends on a file or module to understand "
                    "potential impact of changes.",
    )
    impact_parser.add_argument(
        "repo_path",
        type=str,
        help="Path to the repository",
    )
    impact_parser.add_argument(
        "target",
        type=str,
        help="File or module to analyze impact for",
    )
    impact_parser.set_defaults(func=cmd_impact)
    
    # find command
    find_parser = subparsers.add_parser(
        "find",
        help="Search for files or symbols",
        description="Search for files, symbols, or content matching a query.",
    )
    find_parser.add_argument(
        "repo_path",
        type=str,
        help="Path to the repository",
    )
    find_parser.add_argument(
        "query",
        type=str,
        help="Search query",
    )
    find_parser.set_defaults(func=cmd_find)
    
    return parser


def main(argv: list[str] | None = None) -> int:
    """
    Main entry point for the CLI.
    
    Args:
        argv: Command line arguments (defaults to sys.argv[1:])
    
    Returns:
        Exit code (0 for success, non-zero for errors)
    """
    parser = create_parser()
    args = parser.parse_args(argv)
    
    if args.command is None:
        parser.print_help()
        return 0
    
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
