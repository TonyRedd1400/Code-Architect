"""Tests for CLI commands."""

import sqlite3
from pathlib import Path

import pytest

from codebase_brain.cli import NOT_IMPLEMENTED_EXIT, create_parser, main


FIXTURE_REPO = Path(__file__).parent / "fixtures" / "sample_repo"


def test_cli_help_lists_commands():
    help_text = create_parser().format_help()
    assert "codebrain" in help_text
    for command in ("analyze", "overview", "explain", "impact", "find"):
        assert command in help_text


def test_cli_version(capsys):
    with pytest.raises(SystemExit) as exc_info:
        main(["--version"])
    assert exc_info.value.code == 0
    assert "0.1.0" in capsys.readouterr().out


def test_cli_no_command_shows_help(capsys):
    assert main([]) == 0
    assert "usage:" in capsys.readouterr().out.lower()


def test_cli_analyze_indexes_fixture(tmp_path, capsys):
    db_path = tmp_path / "analysis.db"

    result = main(["analyze", str(FIXTURE_REPO), "--db-path", str(db_path)])

    assert result == 0
    output = capsys.readouterr().out
    assert "Files indexed: 5" in output
    assert str(db_path.resolve()) in output
    conn = sqlite3.connect(db_path)
    try:
        assert conn.execute("SELECT COUNT(*) FROM repos").fetchone()[0] == 1
        assert conn.execute("SELECT COUNT(*) FROM files").fetchone()[0] == 5
        languages = {
            row[0] for row in conn.execute("SELECT DISTINCT language FROM files")
        }
        assert "javascript" in languages
    finally:
        conn.close()


def test_cli_analyze_is_idempotent(tmp_path):
    db_path = tmp_path / "analysis.db"
    args = ["analyze", str(FIXTURE_REPO), "--db-path", str(db_path)]

    assert main(args) == 0
    assert main(args) == 0

    conn = sqlite3.connect(db_path)
    try:
        assert conn.execute("SELECT COUNT(*) FROM repos").fetchone()[0] == 1
        assert conn.execute("SELECT COUNT(*) FROM files").fetchone()[0] == 5
    finally:
        conn.close()


def test_cli_overview_reports_repository(capsys):
    assert main(["overview", str(FIXTURE_REPO)]) == 0
    output = capsys.readouterr().out
    assert "Repository: sample-repo" in output
    assert "Total files: 5" in output
    assert "javascript: 3" in output
    assert "package.json (javascript)" in output


@pytest.mark.parametrize(
    ("command", "extra_arg"),
    [("explain", "src/app.js"), ("impact", "src/app.js"), ("find", "app")],
)
def test_pending_commands_fail_explicitly(command, extra_arg, capsys):
    assert main([command, str(FIXTURE_REPO), extra_arg]) == NOT_IMPLEMENTED_EXIT
    assert "not implemented" in capsys.readouterr().err


def test_cli_analyze_nonexistent_path(capsys):
    assert main(["analyze", "path-that-does-not-exist"]) == 1
    assert "does not exist" in capsys.readouterr().err
