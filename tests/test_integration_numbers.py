"""
Integration tests for numeric literal handling.
Tests integers, decimals, scientific notation, and edge cases.
"""

import pytest
from multilang_lexer import Lexer, TokenType


class TestNumberHandling:
    """Test various numeric literal scenarios."""

    def test_integer_numbers(self):
        """Test integer literals."""
        lexer = Lexer("0 1 42 999 10000")
        tokens = lexer.tokenize()
        numbers = [t for t in tokens if t.type == TokenType.TK_NUMBER]
        assert len(numbers) == 5
        assert numbers[0].value == 0.0
        assert numbers[1].value == 1.0
        assert numbers[2].value == 42.0
        assert numbers[3].value == 999.0
        assert numbers[4].value == 10000.0

    def test_decimal_numbers(self):
        """Test decimal literals."""
        lexer = Lexer("3.14 0.5 .25 100.001")
        tokens = lexer.tokenize()
        numbers = [t for t in tokens if t.type == TokenType.TK_NUMBER]
        assert len(numbers) == 4
        assert abs(numbers[0].value - 3.14) < 0.001
        assert numbers[1].value == 0.5
        assert numbers[2].value == 0.25
        assert abs(numbers[3].value - 100.001) < 0.001

    def test_scientific_notation(self):
        """Test scientific notation."""
        lexer = Lexer("1e10 1E10 1e-5 1.5e3 2.5E-2")
        tokens = lexer.tokenize()
        numbers = [t for t in tokens if t.type == TokenType.TK_NUMBER]
        assert len(numbers) == 5
        assert numbers[0].value == 1e10
        assert numbers[1].value == 1e10
        assert numbers[2].value == 1e-5
        assert numbers[3].value == 1.5e3
        assert numbers[4].value == 2.5e-2

    def test_numbers_with_operators(self):
        """Test numbers in expressions."""
        lexer = Lexer("1+2-3*4/5")
        tokens = lexer.tokenize()
        numbers = [t for t in tokens if t.type == TokenType.TK_NUMBER]
        operators = [t for t in tokens if t.type < 256 and chr(t.type) in '+-*/']
        assert len(numbers) == 5
        assert len(operators) == 4


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
