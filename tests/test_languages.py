"""
Tests for language loading functionality.
"""

import pytest
from multilang_lexer.languages import load_language


def test_load_english():
    """Test loading English language file."""
    lang = load_language('english')
    assert lang['IF'] == 'if'
    assert lang['FUNCTION'] == 'function'
    assert lang['RETURN'] == 'return'


def test_load_spanish():
    """Test loading Spanish language file."""
    lang = load_language('spanish')
    assert lang['IF'] == 'si'
    assert lang['FUNCTION'] == 'función'
    assert lang['RETURN'] == 'devolver'


def test_load_mandarin():
    """Test loading Mandarin language file."""
    lang = load_language('mandarin')
    assert lang['IF'] == '如果'
    assert lang['FUNCTION'] == '函数'
    assert lang['RETURN'] == '返回'


def test_load_nonexistent_language():
    """Test that loading a non-existent language raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        load_language('klingon')


def test_all_keywords_present():
    """Test that all required keywords are present in each language file."""
    required_keywords = [
        'AND', 'BREAK', 'DO', 'ELSE', 'ELSEIF', 'END', 'FOR', 'FUNCTION',
        'IF', 'IN', 'LOCAL', 'NIL', 'NOT', 'OR', 'REPEAT', 'RETURN', 'THEN',
        'UNTIL', 'WHILE'
    ]

    for language in ['english', 'spanish', 'mandarin']:
        lang = load_language(language)
        for keyword in required_keywords:
            assert keyword in lang, f"{keyword} missing from {language}"
            assert isinstance(lang[keyword], str), f"{keyword} in {language} is not a string"
            assert len(lang[keyword]) > 0, f"{keyword} in {language} is empty"


def test_no_extra_keywords():
    """Test that language files don't have unexpected extra keywords."""
    expected_keywords = {
        'AND', 'BREAK', 'DO', 'ELSE', 'ELSEIF', 'END', 'FOR', 'FUNCTION',
        'IF', 'IN', 'LOCAL', 'NIL', 'NOT', 'OR', 'REPEAT', 'RETURN', 'THEN',
        'UNTIL', 'WHILE'
    }

    for language in ['english', 'spanish', 'mandarin']:
        lang = load_language(language)
        assert set(lang.keys()) == expected_keywords, \
            f"{language} has unexpected keywords: {set(lang.keys()) - expected_keywords}"


def test_keywords_are_unique():
    """Test that all keyword translations are unique within each language."""
    for language in ['english', 'spanish', 'mandarin']:
        lang = load_language(language)
        values = list(lang.values())
        assert len(values) == len(set(values)), \
            f"{language} has duplicate keyword translations"


def test_english_keywords_lowercase():
    """Test that English keywords are lowercase."""
    lang = load_language('english')
    for keyword, translation in lang.items():
        assert translation.islower(), f"English keyword {keyword} is not lowercase: {translation}"


def test_spanish_special_characters():
    """Test that Spanish uses proper special characters."""
    lang = load_language('spanish')
    # Spanish should use 'función' with ó
    assert lang['FUNCTION'] == 'función'
    # Check that it's using proper Spanish keywords
    assert lang['IF'] == 'si'
    assert lang['ELSE'] == 'sino'


def test_mandarin_uses_chinese_characters():
    """Test that Mandarin uses Chinese characters."""
    lang = load_language('mandarin')
    # All Mandarin translations should contain Chinese characters
    for keyword, translation in lang.items():
        # Chinese characters have Unicode values > 127
        assert any(ord(c) > 127 for c in translation), \
            f"Mandarin keyword {keyword} doesn't use Chinese characters: {translation}"


def test_language_file_path_construction():
    """Test that language file paths are constructed correctly."""
    import os
    from multilang_lexer.languages import load_language

    # This should successfully find the file
    lang = load_language('english')
    assert lang is not None


def test_load_language_returns_dict():
    """Test that load_language returns a dictionary."""
    lang = load_language('english')
    assert isinstance(lang, dict)


def test_load_language_case_sensitive():
    """Test that language loading is case-sensitive."""
    # 'english' should work
    lang = load_language('english')
    assert lang is not None

    # 'English' should fail (case mismatch)
    with pytest.raises(FileNotFoundError):
        load_language('English')


def test_keyword_count():
    """Test that each language has exactly 19 keywords."""
    for language in ['english', 'spanish', 'mandarin']:
        lang = load_language(language)
        assert len(lang) == 19, f"{language} should have exactly 19 keywords"
