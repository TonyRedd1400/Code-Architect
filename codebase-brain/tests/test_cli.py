"""Tests for CLI commands."""

import subprocess
import sys


def test_cli_help():
    """Test that CLI shows help without errors."""
    result = subprocess.run(
        [sys.executable, "-m", "codebase_brain.cli", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "codebrain" in result.stdout
    assert "analyze" in result.stdout
    assert "overview" in result.stdout
    assert "explain" in result.stdout
    assert "impact" in result.stdout
    assert "find" in result.stdout


def test_cli_version():
    """Test that CLI shows version."""
    result = subprocess.run(
        [sys.executable, "-m", "codebase_brain.cli", "--version"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "0.1.0" in result.stdout


def test_cli_analyze_help():
    """Test analyze subcommand help."""
    result = subprocess.run(
        [sys.executable, "-m", "codebase_brain.cli", "analyze", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "repo_path" in result.stdout


def test_cli_overview_help():
    """Test overview subcommand help."""
    result = subprocess.run(
        [sys.executable, "-m", "codebase_brain.cli", "overview", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0


def test_cli_explain_help():
    """Test explain subcommand help."""
    result = subprocess.run(
        [sys.executable, "-m", "codebase_brain.cli", "explain", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "target_path" in result.stdout


def test_cli_impact_help():
    """Test impact subcommand help."""
    result = subprocess.run(
        [sys.executable, "-m", "codebase_brain.cli", "impact", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "target" in result.stdout


def test_cli_find_help():
    """Test find subcommand help."""
    result = subprocess.run(
        [sys.executable, "-m", "codebase_brain.cli", "find", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "query" in result.stdout


def test_cli_no_command():
    """Test CLI with no command shows help."""
    result = subprocess.run(
        [sys.executable, "-m", "codebase_brain.cli"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "usage:" in result.stdout.lower() or "commands" in result.stdout.lower()


def test_cli_analyze_nonexistent_path():
    """Test analyze with non-existent path returns error."""
    result = subprocess.run(
        [sys.executable, "-m", "codebase_brain.cli", "analyze", "/nonexistent/path"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1
    assert "Error" in result.stderr or "does not exist" in result.stderr
