"""
Integration tests for operators and identifiers.
Tests all operator types, identifier formats, and keyword conflict resolution.
"""

import pytest
from multilang_lexer import Lexer, Token, TokenType
from multilang_lexer.detokenizer import Detokenizer


class TestOperators:
    """Test all operator types."""

    def test_arithmetic_operators(self):
        """Test arithmetic operators."""
        lexer = Lexer("+ - * / ^")
        tokens = lexer.tokenize()
        ops = [chr(t.type) for t in tokens if t.type < 256]
        assert '+' in ops
        assert '-' in ops
        assert '*' in ops
        assert '/' in ops
        assert '^' in ops

    def test_comparison_operators(self):
        """Test comparison operators."""
        lexer = Lexer("== ~= < > <= >=")
        tokens = lexer.tokenize()
        assert any(t.type == TokenType.TK_EQ for t in tokens)
        assert any(t.type == TokenType.TK_NE for t in tokens)
        assert any(t.type == ord('<') for t in tokens)
        assert any(t.type == ord('>') for t in tokens)
        assert any(t.type == TokenType.TK_LE for t in tokens)
        assert any(t.type == TokenType.TK_GE for t in tokens)

    def test_logical_operators(self):
        """Test logical operators."""
        lexer = Lexer("and or not")
        tokens = lexer.tokenize()
        assert any(t.type == TokenType.TK_AND for t in tokens)
        assert any(t.type == TokenType.TK_OR for t in tokens)
        assert any(t.type == TokenType.TK_NOT for t in tokens)

    def test_string_operators(self):
        """Test string concatenation and variadic operators."""
        lexer = Lexer(".. ...")
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.TK_CONCAT
        assert tokens[1].type == TokenType.TK_DOTS

    def test_assignment_and_brackets(self):
        """Test assignment and bracket operators."""
        lexer = Lexer("= ( ) { } [ ]")
        tokens = lexer.tokenize()
        ops = [chr(t.type) for t in tokens if t.type < 256]
        assert '=' in ops
        assert '(' in ops
        assert ')' in ops
        assert '{' in ops
        assert '}' in ops
        assert '[' in ops
        assert ']' in ops


class TestIdentifiers:
    """Test identifier handling."""

    def test_simple_identifiers(self):
        """Test simple ASCII identifiers."""
        lexer = Lexer("x y z abc def ghi")
        tokens = lexer.tokenize()
        names = [t for t in tokens if t.type == TokenType.TK_NAME]
        assert len(names) == 6
        assert [n.value for n in names] == ["x", "y", "z", "abc", "def", "ghi"]

    def test_identifiers_with_underscores(self):
        """Test identifiers with underscores."""
        lexer = Lexer("_x x_ _x_ __private")
        tokens = lexer.tokenize()
        names = [t for t in tokens if t.type == TokenType.TK_NAME]
        assert len(names) == 4

    def test_identifiers_with_numbers(self):
        """Test identifiers with numbers."""
        lexer = Lexer("x1 x2y3 var123")
        tokens = lexer.tokenize()
        names = [t for t in tokens if t.type == TokenType.TK_NAME]
        assert len(names) == 3
        assert names[0].value == "x1"
        assert names[1].value == "x2y3"
        assert names[2].value == "var123"

    def test_unicode_identifiers(self):
        """Test Unicode identifiers."""
        lexer = Lexer("变量 función переменная")
        tokens = lexer.tokenize()
        names = [t for t in tokens if t.type == TokenType.TK_NAME]
        assert len(names) == 3

    def test_mixed_identifiers(self):
        """Test mixed ASCII and Unicode identifiers."""
        lexer = Lexer("test变量 función_x var_Ω")
        tokens = lexer.tokenize()
        names = [t for t in tokens if t.type == TokenType.TK_NAME]
        assert len(names) == 3


class TestKeywordConflictResolution:
    """Test identifier conflict resolution when translating languages."""

    def test_identifier_conflicts_with_target_keywords(self):
        """Test that identifiers conflicting with target keywords are renamed."""
        # Code with identifier named "si" (which is "if" in Spanish)
        english_code = "local si = 5"
        
        lexer = Lexer(english_code, language='english')
        tokens = lexer.tokenize()
        
        # Translate to Spanish - "si" should be renamed since it's a Spanish keyword
        spanish_code = Detokenizer.detokenize(tokens, target_language='spanish')
        
        # The identifier should be renamed (prefixed with underscores)
        assert '_si' in spanish_code or 'si' not in spanish_code.split('local')[1].split('=')[0]

    def test_multiple_identifier_conflicts(self):
        """Test multiple conflicting identifiers."""
        # Use Spanish keywords as identifiers in English code
        english_code = "local si = 1 local entonces = 2"
        
        lexer = Lexer(english_code, language='english')
        tokens = lexer.tokenize()
        spanish_code = Detokenizer.detokenize(tokens, target_language='spanish')
        
        # Both should be renamed
        assert '_si' in spanish_code or '_entonces' in spanish_code


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
