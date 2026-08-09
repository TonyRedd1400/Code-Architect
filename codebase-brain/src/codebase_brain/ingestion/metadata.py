"""Metadata extraction from repositories."""

import json
from pathlib import Path
from typing import Any


def detect_metadata(repo_path: Path | str) -> dict[str, Any]:
    """
    Extract metadata from a repository.
    
    Looks for common metadata files and extracts relevant information:
    - package.json: name, version, description, author, license
    - pyproject.toml: project name, version, description
    - README.md: presence and first few lines
    - LICENSE: type of license
    
    Args:
        repo_path: Path to the repository root
        
    Returns:
        Dictionary with metadata:
        {
            "name": "repo-name",
            "version": "1.0.0",
            "description": "...",
            "license": "MIT",
            "has_readme": True,
            "ecosystem": "javascript",
            ...
        }
        
    Example:
        metadata = detect_metadata("/path/to/repo")
        print(f"Project: {metadata.get('name', 'unknown')}")
    """
    if isinstance(repo_path, str):
        repo_path = Path(repo_path)
    
    repo_path = repo_path.resolve()
    metadata: dict[str, Any] = {
        "path": str(repo_path),
        "name": repo_path.name,
    }
    
    # Check package.json
    package_json_path = repo_path / "package.json"
    if package_json_path.exists():
        try:
            with open(package_json_path, "r", encoding="utf-8") as f:
                package_data = json.load(f)
            
            metadata.update({
                "name": package_data.get("name", metadata["name"]),
                "version": package_data.get("version", "0.0.0"),
                "description": package_data.get("description"),
                "author": package_data.get("author"),
                "license": package_data.get("license"),
                "homepage": package_data.get("homepage"),
                "repository": package_data.get("repository"),
                "keywords": package_data.get("keywords", []),
                "ecosystem": "javascript",
            })
        except (json.JSONDecodeError, OSError):
            pass
    
    # Check pyproject.toml (basic parsing)
    pyproject_toml = repo_path / "pyproject.toml"
    if pyproject_toml.exists():
        try:
            with open(pyproject_toml, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Very basic parsing - just look for common patterns
            for line in content.split("\n"):
                line = line.strip()
                if line.startswith("name"):
                    if "=" in line:
                        value = line.split("=")[1].strip().strip('"\'')
                        metadata["name"] = value
                elif line.startswith("version"):
                    if "=" in line:
                        value = line.split("=")[1].strip().strip('"\'')
                        metadata["version"] = value
                elif line.startswith("description"):
                    if "=" in line:
                        value = line.split("=")[1].strip().strip('"\'')
                        metadata["description"] = value
            
            if "ecosystem" not in metadata:
                metadata["ecosystem"] = "python"
                
        except OSError:
            pass
    
    # Check for README
    readme_extensions = [".md", ".rst", ".txt"]
    for ext in readme_extensions:
        readme_path = repo_path / f"README{ext}"
        if readme_path.exists():
            metadata["has_readme"] = True
            metadata["readme_path"] = f"README{ext}"
            
            # Read first few lines for preview
            try:
                with open(readme_path, "r", encoding="utf-8") as f:
                    first_lines = f.read(500)
                    metadata["readme_preview"] = first_lines.strip()
            except OSError:
                pass
            break
    
    # Check for LICENSE
    license_names = ["LICENSE", "LICENSE.txt", "LICENSE.md", "COPYING"]
    for license_name in license_names:
        license_path = repo_path / license_name
        if license_path.exists():
            metadata["has_license"] = True
            metadata["license_path"] = license_name
            
            # Try to detect license type from content
            try:
                with open(license_path, "r", encoding="utf-8") as f:
                    content = f.read(200).upper()
                
                if "MIT" in content:
                    metadata["license"] = "MIT"
                elif "APACHE" in content:
                    metadata["license"] = "Apache-2.0"
                elif "GPL" in content:
                    metadata["license"] = "GPL"
                elif "BSD" in content:
                    metadata["license"] = "BSD"
                elif "ISC" in content:
                    metadata["license"] = "ISC"
                    
            except OSError:
                pass
            break
    
    # If no ecosystem detected, try to infer from files
    if "ecosystem" not in metadata:
        ecosystem = infer_ecosystem(repo_path)
        if ecosystem:
            metadata["ecosystem"] = ecosystem
    
    return metadata


def infer_ecosystem(repo_path: Path) -> str | None:
    """
    Infer the primary ecosystem from repository contents.
    
    Args:
        repo_path: Path to the repository root
        
    Returns:
        Ecosystem name or None
    """
    indicators = {
        "javascript": ["package.json", "index.js", "node_modules"],
        "python": ["setup.py", "pyproject.toml", "requirements.txt", "__init__.py"],
        "go": ["go.mod", "main.go", "go.sum"],
        "rust": ["Cargo.toml", "src/main.rs"],
        "java": ["pom.xml", "build.gradle", "build.gradle.kts"],
        "ruby": ["Gemfile", "Rakefile", "*.gemspec"],
    }
    
    scores: dict[str, int] = {}
    
    for ecosystem, files in indicators.items():
        score = 0
        for file_pattern in files:
            if "*" in file_pattern:
                # Simple glob check
                if any(repo_path.glob(file_pattern)):
                    score += 1
            else:
                if (repo_path / file_pattern).exists():
                    score += 1
        if score > 0:
            scores[ecosystem] = score
    
    if scores:
        return max(scores.keys(), key=lambda k: scores[k])
    
    return None
