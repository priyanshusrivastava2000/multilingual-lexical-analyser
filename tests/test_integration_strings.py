"""
Integration tests for string literal handling.
Tests various string formats, escape sequences, and edge cases.
"""

import pytest
from multilang_lexer import Lexer, TokenType


class TestStringHandling:
    """Test various string literal scenarios."""

    def test_empty_string(self):
        """Test empty string literals."""
        lexer = Lexer('""')
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.TK_STRING
        assert tokens[0].value == ""

    def test_string_with_escapes(self):
        """Test strings with escape sequences."""
        code = r'"hello\nworld\t\"\\"'
        lexer = Lexer(code, language='english')
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.TK_STRING
        assert '\n' in tokens[0].value
        assert '\t' in tokens[0].value

    def test_string_with_unicode(self):
        """Test strings with Unicode characters."""
        lexer = Lexer('"你好世界"')
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.TK_STRING
        assert tokens[0].value == "你好世界"

    def test_long_string(self):
        """Test long string literals with [[...]]."""
        code = "[[This is a long string]]"
        lexer = Lexer(code, language='english')
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.TK_STRING
        assert tokens[0].value == "This is a long string"

    def test_long_string_with_newlines(self):
        """Test long strings with embedded newlines."""
        code = """[[Line 1
Line 2
Line 3]]"""
        lexer = Lexer(code, language='english')
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.TK_STRING
        assert "Line 1" in tokens[0].value
        assert "Line 2" in tokens[0].value
        assert "Line 3" in tokens[0].value

    def test_nested_long_strings(self):
        """Test nested long string literals."""
        code = "[[outer [[inner]] outer]]"
        lexer = Lexer(code, language='english')
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.TK_STRING
        assert tokens[0].value == "outer [[inner]] outer"

    def test_single_vs_double_quotes(self):
        """Test both single and double quoted strings."""
        code = "'single' \"double\""
        lexer = Lexer(code, language='english')
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.TK_STRING
        assert tokens[0].value == "single"
        assert tokens[1].type == TokenType.TK_STRING
        assert tokens[1].value == "double"

    def test_string_with_all_escapes(self):
        """Test all supported escape sequences."""
        code = r'"\a\b\f\n\r\t\v\\\"\'"'
        lexer = Lexer(code, language='english')
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.TK_STRING
        value = tokens[0].value
        assert '\a' in value  # bell
        assert '\b' in value  # backspace
        assert '\f' in value  # form feed
        assert '\n' in value  # newline
        assert '\r' in value  # carriage return
        assert '\t' in value  # tab
        assert '\v' in value  # vertical tab

    def test_numeric_escape_sequences(self):
        """Test numeric escape sequences in strings."""
        code = r'"\065\066\067"'  # ASCII codes for "ABC"
        lexer = Lexer(code, language='english')
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.TK_STRING
        assert tokens[0].value == "ABC"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
