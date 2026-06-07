"""
Tests for Token and TokenType classes.
"""

import pytest
from multilang_lexer import Token, TokenType


def test_token_repr_with_value():
    """Test Token repr for tokens with values."""
    token = Token(TokenType.TK_NAME, 'factorial', line=5)
    assert 'factorial' in repr(token)
    assert 'line=5' in repr(token)


def test_token_repr_without_value():
    """Test Token repr for tokens without values."""
    token = Token(TokenType.TK_IF, line=3)
    assert 'if' in repr(token)
    assert 'line=3' in repr(token)


def test_token_repr_single_char():
    """Test Token repr for single character tokens."""
    token = Token(ord('('), line=1)
    assert "'('" in repr(token)


def test_token_number():
    """Test number token."""
    token = Token(TokenType.TK_NUMBER, 42.5, line=2)
    assert token.type == TokenType.TK_NUMBER
    assert token.value == 42.5
    assert token.line == 2


def test_token_string():
    """Test string token."""
    token = Token(TokenType.TK_STRING, "hello", line=4)
    assert token.type == TokenType.TK_STRING
    assert token.value == "hello"
    assert token.line == 4


def test_token_keyword():
    """Test keyword token."""
    token = Token(TokenType.TK_FUNCTION, line=1)
    assert token.type == TokenType.TK_FUNCTION
    assert token.value is None


def test_token_type_enum_values():
    """Test that TokenType enum values start at 257."""
    assert TokenType.FIRST_RESERVED == 257
    assert TokenType.TK_AND == 257
    assert TokenType.TK_BREAK == 258


def test_token_type_ordering():
    """Test that token types have correct ordering."""
    # Keywords should be sequential
    assert TokenType.TK_BREAK == TokenType.TK_AND + 1
    assert TokenType.TK_DO == TokenType.TK_BREAK + 1


def test_token_strings_dict():
    """Test TOKEN_STRINGS dictionary."""
    from multilang_lexer.tokens import TOKEN_STRINGS
    assert TokenType.TK_IF in TOKEN_STRINGS
    assert TOKEN_STRINGS[TokenType.TK_IF] == "if"
    assert TOKEN_STRINGS[TokenType.TK_NUMBER] == "<number>"
    assert TOKEN_STRINGS[TokenType.TK_STRING] == "<string>"
    assert TOKEN_STRINGS[TokenType.TK_EOS] == "<eof>"


def test_keyword_to_token_dict():
    """Test KEYWORD_TO_TOKEN dictionary."""
    from multilang_lexer.tokens import KEYWORD_TO_TOKEN
    assert "IF" in KEYWORD_TO_TOKEN
    assert KEYWORD_TO_TOKEN["IF"] == TokenType.TK_IF
    assert "FUNCTION" in KEYWORD_TO_TOKEN
    assert KEYWORD_TO_TOKEN["FUNCTION"] == TokenType.TK_FUNCTION


def test_all_keywords_in_dicts():
    """Test that all keywords from KEYWORD_TO_TOKEN are in TOKEN_STRINGS."""
    from multilang_lexer.tokens import KEYWORD_TO_TOKEN, TOKEN_STRINGS
    for keyword, token_type in KEYWORD_TO_TOKEN.items():
        assert token_type in TOKEN_STRINGS
        # Verify TOKEN_STRINGS has the lowercase version
        assert TOKEN_STRINGS[token_type] == keyword.lower()


def test_token_strings_completeness():
    """Verify TOKEN_STRINGS is correctly generated from KEYWORD_TO_TOKEN and operators."""
    from multilang_lexer.tokens import KEYWORD_TO_TOKEN, TOKEN_STRINGS

    # All keyword TokenTypes should be in TOKEN_STRINGS with lowercase values
    for keyword, token_type in KEYWORD_TO_TOKEN.items():
        assert token_type in TOKEN_STRINGS, f"TokenType for {keyword} not in TOKEN_STRINGS"
        assert TOKEN_STRINGS[token_type] == keyword.lower(), \
            f"Expected TOKEN_STRINGS[{token_type}] to be '{keyword.lower()}', got '{TOKEN_STRINGS[token_type]}'"

    # Verify operator tokens are present
    assert TokenType.TK_CONCAT in TOKEN_STRINGS
    assert TOKEN_STRINGS[TokenType.TK_CONCAT] == ".."
    assert TokenType.TK_DOTS in TOKEN_STRINGS
    assert TOKEN_STRINGS[TokenType.TK_DOTS] == "..."
    assert TokenType.TK_EQ in TOKEN_STRINGS
    assert TOKEN_STRINGS[TokenType.TK_EQ] == "=="
    assert TokenType.TK_GE in TOKEN_STRINGS
    assert TOKEN_STRINGS[TokenType.TK_GE] == ">="
    assert TokenType.TK_LE in TOKEN_STRINGS
    assert TOKEN_STRINGS[TokenType.TK_LE] == "<="
    assert TokenType.TK_NE in TOKEN_STRINGS
    assert TOKEN_STRINGS[TokenType.TK_NE] == "~="

    # Verify special tokens are present
    assert TokenType.TK_NUMBER in TOKEN_STRINGS
    assert TOKEN_STRINGS[TokenType.TK_NUMBER] == "<number>"
    assert TokenType.TK_STRING in TOKEN_STRINGS
    assert TOKEN_STRINGS[TokenType.TK_STRING] == "<string>"
    assert TokenType.TK_NAME in TOKEN_STRINGS
    assert TOKEN_STRINGS[TokenType.TK_NAME] == "<name>"
    assert TokenType.TK_EOS in TOKEN_STRINGS
    assert TOKEN_STRINGS[TokenType.TK_EOS] == "<eof>"


def test_token_equality():
    """Test token equality based on type, value, and line."""
    token1 = Token(TokenType.TK_NAME, "test", line=1)
    token2 = Token(TokenType.TK_NAME, "test", line=1)
    # Dataclass should provide equality
    assert token1 == token2


def test_token_inequality_different_type():
    """Test tokens with different types are not equal."""
    token1 = Token(TokenType.TK_NAME, "test", line=1)
    token2 = Token(TokenType.TK_STRING, "test", line=1)
    assert token1 != token2


def test_token_inequality_different_value():
    """Test tokens with different values are not equal."""
    token1 = Token(TokenType.TK_NAME, "test1", line=1)
    token2 = Token(TokenType.TK_NAME, "test2", line=1)
    assert token1 != token2


def test_token_inequality_different_line():
    """Test tokens with different line numbers are not equal."""
    token1 = Token(TokenType.TK_NAME, "test", line=1)
    token2 = Token(TokenType.TK_NAME, "test", line=2)
    assert token1 != token2


def test_token_single_char_values():
    """Test single character token values."""
    for char in "(){}[];,.+-*/<>=~":
        token = Token(ord(char), line=1)
        assert token.type == ord(char)
        assert token.type < 256


def test_token_operator_types():
    """Test multi-character operator token types."""
    assert TokenType.TK_CONCAT == 276
    assert TokenType.TK_DOTS == 277
    assert TokenType.TK_EQ == 278
    assert TokenType.TK_GE == 279
    assert TokenType.TK_LE == 280
    assert TokenType.TK_NE == 281


def test_token_special_types():
    """Test special token types."""
    assert TokenType.TK_NUMBER == 282
    assert TokenType.TK_STRING == 283
    assert TokenType.TK_NAME == 284
    assert TokenType.TK_EOS == 285
