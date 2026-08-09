"""Ingestion layer for extracting information from repositories."""

from .scanner import scan_repository
from .languages import detect_languages, get_language_from_extension
from .entrypoints import detect_entrypoints
from .metadata import detect_metadata

__all__ = [
    "scan_repository",
    "detect_languages",
    "get_language_from_extension",
    "detect_entrypoints",
    "detect_metadata",
]
