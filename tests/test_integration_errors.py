"""
Integration tests for error detection and reporting.
Tests various error conditions and proper error messages.
"""

import pytest
from multilang_lexer import Lexer, LexerError


class TestErrorHandling:
    """Test error detection and reporting."""

    def test_unfinished_string(self):
        """Test error on unfinished string."""
        with pytest.raises(LexerError) as exc_info:
            lexer = Lexer('"hello')
            lexer.tokenize()
        assert "unfinished string" in str(exc_info.value)

    def test_unfinished_long_string(self):
        """Test error on unfinished long string."""
        with pytest.raises(LexerError) as exc_info:
            lexer = Lexer("[[hello")
            lexer.tokenize()
        assert "unfinished long string" in str(exc_info.value)

    def test_invalid_dollar_sign(self):
        """Test error on invalid dollar sign."""
        with pytest.raises(LexerError) as exc_info:
            lexer = Lexer("$")
            lexer.tokenize()
        assert "$" in str(exc_info.value)

    def test_malformed_number(self):
        """Test error on malformed number with double dots."""
        with pytest.raises(LexerError) as exc_info:
            lexer = Lexer("3..")
            lexer.tokenize()
        assert "ambiguous syntax" in str(exc_info.value)

    def test_numeric_escape_too_large(self):
        """Test error on numeric escape sequence too large."""
        with pytest.raises(LexerError) as exc_info:
            lexer = Lexer(r'"\999"')
            lexer.tokenize()
        assert "too large" in str(exc_info.value)

    def test_unfinished_string_with_newline(self):
        """Test error on string with unescaped newline."""
        with pytest.raises(LexerError) as exc_info:
            code = '"hello\nworld"'
            lexer = Lexer(code)
            lexer.tokenize()
        assert "unfinished string" in str(exc_info.value)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
