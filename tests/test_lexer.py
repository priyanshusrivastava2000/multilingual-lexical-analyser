"""
Tests for the Lexer class.
"""

import pytest
from multilang_lexer import Lexer, Token, TokenType, LexerError


def test_lexer_simple_identifier():
    """Test tokenizing a simple identifier."""
    lexer = Lexer("hello")
    tokens = lexer.tokenize()
    assert len(tokens) == 2  # NAME + EOS
    assert tokens[0].type == TokenType.TK_NAME
    assert tokens[0].value == "hello"
    assert tokens[1].type == TokenType.TK_EOS


def test_lexer_number():
    """Test tokenizing numbers."""
    lexer = Lexer("42 3.14 .5 1e10")
    tokens = lexer.tokenize()
    numbers = [t for t in tokens if t.type == TokenType.TK_NUMBER]
    assert len(numbers) == 4
    assert numbers[0].value == 42.0
    assert numbers[1].value == 3.14
    assert numbers[2].value == 0.5
    assert numbers[3].value == 1e10


def test_lexer_string():
    """Test tokenizing strings."""
    lexer = Lexer('"hello" \'world\'')
    tokens = lexer.tokenize()
    strings = [t for t in tokens if t.type == TokenType.TK_STRING]
    assert len(strings) == 2
    assert strings[0].value == "hello"
    assert strings[1].value == "world"


def test_lexer_operators():
    """Test tokenizing operators."""
    lexer = Lexer("== ~= <= >= .. ...")
    tokens = lexer.tokenize()
    assert tokens[0].type == TokenType.TK_EQ
    assert tokens[1].type == TokenType.TK_NE
    assert tokens[2].type == TokenType.TK_LE
    assert tokens[3].type == TokenType.TK_GE
    assert tokens[4].type == TokenType.TK_CONCAT
    assert tokens[5].type == TokenType.TK_DOTS


def test_lexer_english_keywords():
    """Test tokenizing English keywords."""
    lexer = Lexer("if then else end function local")
    tokens = lexer.tokenize()
    assert tokens[0].type == TokenType.TK_IF
    assert tokens[1].type == TokenType.TK_THEN
    assert tokens[2].type == TokenType.TK_ELSE
    assert tokens[3].type == TokenType.TK_END
    assert tokens[4].type == TokenType.TK_FUNCTION
    assert tokens[5].type == TokenType.TK_LOCAL


def test_lexer_spanish_keywords():
    """Test tokenizing Spanish keywords."""
    lexer = Lexer("si entonces sino fin función local", language='spanish')
    tokens = lexer.tokenize()
    assert tokens[0].type == TokenType.TK_IF
    assert tokens[1].type == TokenType.TK_THEN
    assert tokens[2].type == TokenType.TK_ELSE
    assert tokens[3].type == TokenType.TK_END
    assert tokens[4].type == TokenType.TK_FUNCTION
    assert tokens[5].type == TokenType.TK_LOCAL


def test_lexer_mandarin_keywords():
    """Test tokenizing Mandarin keywords."""
    lexer = Lexer("如果 那么 否则 结束 函数 本地", language='mandarin')
    tokens = lexer.tokenize()
    assert tokens[0].type == TokenType.TK_IF
    assert tokens[1].type == TokenType.TK_THEN
    assert tokens[2].type == TokenType.TK_ELSE
    assert tokens[3].type == TokenType.TK_END
    assert tokens[4].type == TokenType.TK_FUNCTION
    assert tokens[5].type == TokenType.TK_LOCAL


def test_lexer_comments():
    """Test that comments are properly ignored."""
    lexer = Lexer("x -- this is a comment\ny")
    tokens = lexer.tokenize()
    names = [t for t in tokens if t.type == TokenType.TK_NAME]
    assert len(names) == 2
    assert names[0].value == "x"
    assert names[1].value == "y"


def test_lexer_line_numbers():
    """Test that line numbers are tracked correctly."""
    lexer = Lexer("x\ny\nz")
    tokens = lexer.tokenize()
    assert tokens[0].line == 1
    assert tokens[1].line == 2
    assert tokens[2].line == 3


def test_lexer_error_unfinished_string():
    """Test error handling for unfinished string."""
    with pytest.raises(LexerError) as exc_info:
        lexer = Lexer('"hello')
        lexer.tokenize()
    assert "unfinished string" in str(exc_info.value)


def test_lexer_complex_expression():
    """Test tokenizing a complex expression."""
    code = "factorial(n - 1) * n"
    lexer = Lexer(code)
    tokens = lexer.tokenize()

    # Verify token sequence
    assert tokens[0].type == TokenType.TK_NAME
    assert tokens[0].value == "factorial"
    assert tokens[1].type == ord('(')
    assert tokens[2].type == TokenType.TK_NAME
    assert tokens[2].value == "n"
    assert tokens[3].type == ord('-')
    assert tokens[4].type == TokenType.TK_NUMBER
    assert tokens[4].value == 1.0
    assert tokens[5].type == ord(')')
    assert tokens[6].type == ord('*')
    assert tokens[7].type == TokenType.TK_NAME
    assert tokens[7].value == "n"
