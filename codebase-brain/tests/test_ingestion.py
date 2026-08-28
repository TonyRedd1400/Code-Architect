"""Functional tests for repository ingestion."""

from pathlib import Path

from codebase_brain.analysis.overview import get_overview
from codebase_brain.ingestion import (
    detect_entrypoints,
    detect_languages,
    detect_metadata,
    scan_repository,
)


FIXTURE_REPO = Path(__file__).parent / "fixtures" / "sample_repo"


def test_scan_repository_ignores_hidden_directories(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "app.py").write_text("print('ok')\n", encoding="utf-8")
    hidden = repo / ".git"
    hidden.mkdir()
    (hidden / "config").write_text("ignored", encoding="utf-8")

    result = scan_repository(repo)

    assert [file_info["path"] for file_info in result.files] == ["app.py"]


def test_detect_languages_for_fixture():
    result = detect_languages(FIXTURE_REPO)
    assert result["primary_language"] == "javascript"
    assert result["languages"] == {
        "javascript": 3,
        "json": 1,
        "markdown": 1,
    }


def test_detect_entrypoint_and_metadata_for_fixture():
    entrypoints = detect_entrypoints(FIXTURE_REPO)
    metadata = detect_metadata(FIXTURE_REPO)

    assert entrypoints[0]["entrypoint"] == "index.js"
    assert metadata["name"] == "sample-repo"
    assert metadata["ecosystem"] == "javascript"


def test_overview_uses_real_ingestion_data():
    overview = get_overview(FIXTURE_REPO)
    assert overview["total_files"] == 5
    assert overview["primary_language"] == "javascript"
    assert overview["directories"] == ["src"]
    assert overview["entrypoints"][0]["entrypoint"] == "index.js"
