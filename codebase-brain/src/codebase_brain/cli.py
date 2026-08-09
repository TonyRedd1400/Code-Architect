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
import sys
from pathlib import Path


def cmd_analyze(args: argparse.Namespace) -> int:
    """Handle the 'analyze' subcommand."""
    repo_path = Path(args.repo_path).resolve()
    
    if not repo_path.exists():
        print(f"Error: Repository path does not exist: {repo_path}", file=sys.stderr)
        return 1
    
    if not repo_path.is_dir():
        print(f"Error: Repository path is not a directory: {repo_path}", file=sys.stderr)
        return 1
    
    # TODO: Implement full repository analysis
    # - Scan repository files
    # - Detect languages
    # - Find entrypoints
    # - Create SQLite database
    # - Build dependency graph
    print(f"TODO: implement analyze for {repo_path}")
    return 0


def cmd_overview(args: argparse.Namespace) -> int:
    """Handle the 'overview' subcommand."""
    repo_path = Path(args.repo_path).resolve()
    
    if not repo_path.exists():
        print(f"Error: Repository path does not exist: {repo_path}", file=sys.stderr)
        return 1
    
    # TODO: Implement repository overview
    # - Show file counts by language
    # - Show directory structure
    # - Show entrypoints found
    # - Show basic statistics
    print(f"TODO: implement overview for {repo_path}")
    return 0


def cmd_explain(args: argparse.Namespace) -> int:
    """Handle the 'explain' subcommand."""
    repo_path = Path(args.repo_path).resolve()
    target = args.target_path
    
    if not repo_path.exists():
        print(f"Error: Repository path does not exist: {repo_path}", file=sys.stderr)
        return 1
    
    # TODO: Implement file/module explanation
    # - Load file from database
    # - Show symbols in file
    # - Show dependencies
    # - Generate summary (future: LLM-based)
    print(f"TODO: implement explain for {target} in {repo_path}")
    return 0


def cmd_impact(args: argparse.Namespace) -> int:
    """Handle the 'impact' subcommand."""
    repo_path = Path(args.repo_path).resolve()
    target = args.target
    
    if not repo_path.exists():
        print(f"Error: Repository path does not exist: {repo_path}", file=sys.stderr)
        return 1
    
    # TODO: Implement impact analysis
    # - Find what depends on target
    # - Show transitive dependencies
    # - Identify potential breakage
    print(f"TODO: implement impact for {target} in {repo_path}")
    return 0


def cmd_find(args: argparse.Namespace) -> int:
    """Handle the 'find' subcommand."""
    repo_path = Path(args.repo_path).resolve()
    query = args.query
    
    if not repo_path.exists():
        print(f"Error: Repository path does not exist: {repo_path}", file=sys.stderr)
        return 1
    
    # TODO: Implement search functionality
    # - Search file paths
    # - Search symbol names
    # - Search file contents (optional)
    print(f"TODO: implement find for '{query}' in {repo_path}")
    return 0


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
                    "build dependency graph, and store in SQLite database.",
    )
    analyze_parser.add_argument(
        "repo_path",
        type=str,
        help="Path to the repository to analyze",
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
