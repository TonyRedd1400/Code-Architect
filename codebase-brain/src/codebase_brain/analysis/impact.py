"""Impact analysis for code changes."""

from pathlib import Path
from typing import Any


def analyze_impact(repo_path: Path | str, target: str) -> dict[str, Any]:
    """
    Analyze the impact of changing a target file or module.
    
    This is a placeholder/stub for the MVP. Future implementation will
    use the dependency graph to find affected files and assess risk.
    
    Args:
        repo_path: Path to the repository root
        target: Target file path or symbol name
        
    Returns:
        Dictionary with impact analysis:
        {
            "target": "...",
            "direct_dependents": [],
            "transitive_dependents": [],
            "risk_level": "unknown",
            "affected_modules": [],
            "tests_covering": [],
        }
        
    Example:
        impact = analyze_impact("/path/to/repo", "src/utils.js")
        print(f"Risk: {impact['risk_level']}")
        print(f"Affected: {len(impact['affected_modules'])} modules")
    """
    if isinstance(repo_path, str):
        repo_path = Path(repo_path)
    
    repo_path = repo_path.resolve()
    
    # TODO: Implement full impact analysis
    # For now, return minimal placeholder
    
    return {
        "target": target,
        "repo_path": str(repo_path),
        "direct_dependents": [],
        "transitive_dependents": [],
        "risk_level": "unknown",
        "affected_modules": [],
        "tests_covering": [],
        "note": "TODO: implement full impact analysis",
    }


def format_impact_text(impact: dict[str, Any]) -> str:
    """
    Format impact analysis as human-readable text.
    
    Args:
        impact: Impact dictionary from analyze_impact()
        
    Returns:
        Formatted text string
    """
    lines = [
        f"Impact Analysis for: {impact.get('target', 'unknown')}",
        "",
        f"Risk Level: {impact.get('risk_level', 'unknown')}",
        "",
        f"Direct dependents: {len(impact.get('direct_dependents', []))}",
        f"Transitive dependents: {len(impact.get('transitive_dependents', []))}",
        "",
        "Affected modules:",
    ]
    
    affected = impact.get("affected_modules", [])
    if affected:
        for mod in affected:
            lines.append(f"  - {mod}")
    else:
        lines.append("  (none)")
    
    lines.append("")
    lines.append("Tests covering this module:")
    tests = impact.get("tests_covering", [])
    if tests:
        for test in tests:
            lines.append(f"  - {test}")
    else:
        lines.append("  (none detected)")
    
    return "\n".join(lines)
