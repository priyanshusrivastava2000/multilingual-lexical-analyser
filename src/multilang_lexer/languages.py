"""
Language loading utilities for the multilingual lexer.
"""

import json
import os


def load_language(language: str) -> dict:
    """
    Load language translations from JSON file.
    Returns a dictionary mapping keyword names to translated keywords.

    Args:
        language: Language name (e.g., 'english', 'spanish', 'mandarin')

    Returns:
        Dictionary mapping canonical keyword names (e.g., 'AND') to
        translated keywords (e.g., 'y' for Spanish)

    Raises:
        FileNotFoundError: If the language file doesn't exist
    """
    package_dir = os.path.dirname(os.path.abspath(__file__))
    lang_file = os.path.join(package_dir, 'languages', f'{language}.json')

    if not os.path.exists(lang_file):
        raise FileNotFoundError(f"Language file not found: {lang_file}")

    with open(lang_file, 'r', encoding='utf-8') as f:
        return json.load(f)
