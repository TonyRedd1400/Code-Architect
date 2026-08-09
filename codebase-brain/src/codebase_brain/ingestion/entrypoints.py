"""Entrypoint detection for various ecosystems."""

import json
from pathlib import Path
from typing import Any


def detect_entrypoints(repo_path: Path | str) -> list[dict[str, Any]]:
    """
    Detect entry points in a repository.
    
    Looks for common entry point patterns across different ecosystems:
    - JavaScript/Node: package.json "main" field, index.js
    - Python: setup.py, __main__.py, pyproject.toml
    - Go: main.go files
    - Rust: Cargo.toml with src/main.rs
    
    Args:
        repo_path: Path to the repository root
        
    Returns:
        List of entrypoint dictionaries:
        [
            {
                "type": "package_json",
                "path": "package.json",
                "entrypoint": "index.js",
                "ecosystem": "javascript",
                "metadata": {...}
            },
            ...
        ]
        
    Example:
        entrypoints = detect_entrypoints("/path/to/repo")
        for ep in entrypoints:
            print(f"{ep['ecosystem']}: {ep['entrypoint']}")
    """
    if isinstance(repo_path, str):
        repo_path = Path(repo_path)
    
    repo_path = repo_path.resolve()
    entrypoints = []
    
    # Check for package.json (JavaScript/Node)
    package_json_path = repo_path / "package.json"
    if package_json_path.exists():
        try:
            with open(package_json_path, "r", encoding="utf-8") as f:
                package_data = json.load(f)
            
            entrypoint = package_data.get("main", "index.js")
            
            # Extract scripts
            scripts = package_data.get("scripts", {})
            
            entrypoints.append({
                "type": "package_json",
                "path": "package.json",
                "absolute_path": str(package_json_path),
                "entrypoint": entrypoint,
                "ecosystem": "javascript",
                "metadata": {
                    "name": package_data.get("name", "unknown"),
                    "version": package_data.get("version", "0.0.0"),
                    "scripts": scripts,
                    "dependencies": package_data.get("dependencies", {}),
                    "devDependencies": package_data.get("devDependencies", {}),
                }
            })
        except (json.JSONDecodeError, OSError):
            pass
    
    # Check for index.js at root (common JS pattern)
    index_js = repo_path / "index.js"
    if index_js.exists() and not any(ep["entrypoint"] == "index.js" for ep in entrypoints):
        entrypoints.append({
            "type": "index_file",
            "path": "index.js",
            "absolute_path": str(index_js),
            "entrypoint": "index.js",
            "ecosystem": "javascript",
            "metadata": {}
        })
    
    # Check for setup.py (Python)
    setup_py = repo_path / "setup.py"
    if setup_py.exists():
        entrypoints.append({
            "type": "setup_py",
            "path": "setup.py",
            "absolute_path": str(setup_py),
            "entrypoint": "setup.py",
            "ecosystem": "python",
            "metadata": {}
        })
    
    # Check for pyproject.toml (Python modern)
    pyproject_toml = repo_path / "pyproject.toml"
    if pyproject_toml.exists():
        entrypoints.append({
            "type": "pyproject_toml",
            "path": "pyproject.toml",
            "absolute_path": str(pyproject_toml),
            "entrypoint": "pyproject.toml",
            "ecosystem": "python",
            "metadata": {}
        })
    
    # Check for __main__.py (Python executable module)
    main_py = repo_path / "__main__.py"
    if main_py.exists():
        entrypoints.append({
            "type": "main_py",
            "path": "__main__.py",
            "absolute_path": str(main_py),
            "entrypoint": "__main__.py",
            "ecosystem": "python",
            "metadata": {}
        })
    
    # Check for main.go (Go)
    main_go = repo_path / "main.go"
    if main_go.exists():
        entrypoints.append({
            "type": "main_go",
            "path": "main.go",
            "absolute_path": str(main_go),
            "entrypoint": "main.go",
            "ecosystem": "go",
            "metadata": {}
        })
    
    # Check for Cargo.toml (Rust)
    cargo_toml = repo_path / "Cargo.toml"
    if cargo_toml.exists():
        entrypoints.append({
            "type": "cargo_toml",
            "path": "Cargo.toml",
            "absolute_path": str(cargo_toml),
            "entrypoint": "src/main.rs",  # Convention
            "ecosystem": "rust",
            "metadata": {}
        })
    
    # Check for pom.xml (Java Maven)
    pom_xml = repo_path / "pom.xml"
    if pom_xml.exists():
        entrypoints.append({
            "type": "pom_xml",
            "path": "pom.xml",
            "absolute_path": str(pom_xml),
            "entrypoint": "src/main/java/**/*App.java",  # Pattern
            "ecosystem": "java",
            "metadata": {}
        })
    
    # Check for build.gradle (Java Gradle)
    build_gradle = repo_path / "build.gradle"
    if build_gradle.exists():
        entrypoints.append({
            "type": "build_gradle",
            "path": "build.gradle",
            "absolute_path": str(build_gradle),
            "entrypoint": "src/main/java/**/*App.java",  # Pattern
            "ecosystem": "java",
            "metadata": {}
        })
    
    return entrypoints


def get_scripts(repo_path: Path | str) -> dict[str, str]:
    """
    Get available scripts/commands from a repository.
    
    Currently focuses on npm scripts from package.json.
    
    Args:
        repo_path: Path to the repository root
        
    Returns:
        Dictionary mapping script names to commands
    """
    if isinstance(repo_path, str):
        repo_path = Path(repo_path)
    
    scripts = {}
    
    # NPM scripts
    package_json_path = repo_path / "package.json"
    if package_json_path.exists():
        try:
            with open(package_json_path, "r", encoding="utf-8") as f:
                package_data = json.load(f)
            
            npm_scripts = package_data.get("scripts", {})
            for name, command in npm_scripts.items():
                scripts[f"npm:{name}"] = command
        except (json.JSONDecodeError, OSError):
            pass
    
    return scripts
