"""LLM prompt templates for future integration.

This module contains prompt templates that will be used when LLM integration
is added. Currently these are just placeholders to establish the interface.
"""

from typing import Any


# Prompt template for explaining a file
EXPLAIN_FILE_PROMPT = """You are an expert software engineer analyzing a codebase.

## Context
Repository: {repo_name}
File: {file_path}
Language: {language}

## File Content
```{language}
{file_content}
```

## Task
Explain what this file does, its purpose, and how it fits into the larger codebase.

## Output Format
Provide your response in the following format:

1. **Purpose**: One-sentence summary of what this file does
2. **Key Components**: List of main functions/classes/variables
3. **Dependencies**: What this file depends on
4. **Dependents**: What likely depends on this file
5. **Complexity**: Assessment of complexity (low/medium/high)
"""

# Prompt template for summarizing a repository
SUMMARIZE_REPO_PROMPT = """You are an expert software engineer analyzing a codebase.

## Repository Structure
{repo_structure}

## Key Files
{key_files}

## Metadata
- Name: {repo_name}
- Primary Language: {primary_language}
- Total Files: {total_files}

## Task
Provide a high-level summary of this repository's purpose and architecture.

## Output Format
1. **Project Type**: What kind of project is this?
2. **Architecture**: Main architectural patterns used
3. **Entry Points**: How is this project executed/used?
4. **Tech Stack**: Technologies and frameworks detected
"""

# Prompt template for impact analysis
IMPACT_ANALYSIS_PROMPT = """You are an expert software engineer analyzing code dependencies.

## Target
File: {target_path}
Change Type: {change_type}

## Dependencies
This file depends on: {dependencies}

## Dependents
These files depend on this target: {dependents}

## Task
Analyze the potential impact of changes to this file.

## Output Format
1. **Risk Level**: low/medium/high
2. **Direct Impact**: Immediate effects
3. **Cascading Effects**: Potential downstream issues
4. **Testing Recommendations**: What tests should be run
"""


def get_prompt_template(template_name: str, **kwargs: Any) -> str:
    """
    Get a prompt template by name and fill in variables.
    
    Args:
        template_name: Name of the template (e.g., 'explain_file')
        **kwargs: Variables to substitute in the template
        
    Returns:
        Formatted prompt string
        
    Example:
        prompt = get_prompt_template(
            'explain_file',
            repo_name='my-project',
            file_path='src/app.py',
            language='python',
            file_content='...',
        )
    """
    templates = {
        "explain_file": EXPLAIN_FILE_PROMPT,
        "summarize_repo": SUMMARIZE_REPO_PROMPT,
        "impact_analysis": IMPACT_ANALYSIS_PROMPT,
    }
    
    if template_name not in templates:
        raise ValueError(f"Unknown template: {template_name}")
    
    template = templates[template_name]
    return template.format(**kwargs)
