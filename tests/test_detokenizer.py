"""
Comprehensive tests for detokenizer module.
Tests token-to-source conversion and cross-language translation.
"""

import pytest
from multilang_lexer.detokenizer import Detokenizer
from multilang_lexer.tokens import Token, TokenType


class TestFormatToken:
    """Tests for format_token() function."""

    def test_format_keyword_english(self):
        """Test formatting keyword token in English."""
        token = Token(TokenType.TK_IF, line=1)
        result = Detokenizer.format_token(token, language='english')
        assert result == "if"

    def test_format_keyword_spanish(self):
        """Test formatting keyword token in Spanish."""
        token = Token(TokenType.TK_IF, line=1)
        result = Detokenizer.format_token(token, language='spanish')
        assert result == "si"

    def test_format_keyword_mandarin(self):
        """Test formatting keyword token in Mandarin."""
        token = Token(TokenType.TK_FUNCTION, line=1)
        result = Detokenizer.format_token(token, language='mandarin')
        assert result == "函数"

    def test_format_all_keywords_english(self):
        """Test formatting all keyword types in English."""
        keywords = [
            (TokenType.TK_AND, "and"),
            (TokenType.TK_BREAK, "break"),
            (TokenType.TK_DO, "do"),
            (TokenType.TK_ELSE, "else"),
            (TokenType.TK_ELSEIF, "elseif"),
            (TokenType.TK_END, "end"),
            (TokenType.TK_FOR, "for"),
            (TokenType.TK_FUNCTION, "function"),
            (TokenType.TK_IF, "if"),
            (TokenType.TK_LOCAL, "local"),
            (TokenType.TK_NIL, "nil"),
            (TokenType.TK_NOT, "not"),
            (TokenType.TK_OR, "or"),
            (TokenType.TK_REPEAT, "repeat"),
            (TokenType.TK_RETURN, "return"),
            (TokenType.TK_THEN, "then"),
            (TokenType.TK_UNTIL, "until"),
            (TokenType.TK_WHILE, "while"),
        ]

        for token_type, expected in keywords:
            token = Token(token_type, line=1)
            result = Detokenizer.format_token(token, language='english')
            assert result == expected, f"Failed for {token_type}"

    def test_format_string_token(self):
        """Test formatting string token."""
        token = Token(TokenType.TK_STRING, "hello world", line=1)
        result = Detokenizer.format_token(token)
        assert result == '"hello world"'

    def test_format_string_with_quotes(self):
        """Test formatting string that contains quotes."""
        token = Token(TokenType.TK_STRING, 'say "hi"', line=1)
        result = Detokenizer.format_token(token)
        assert result == '"say "hi""'

    def test_format_empty_string(self):
        """Test formatting empty string."""
        token = Token(TokenType.TK_STRING, "", line=1)
        result = Detokenizer.format_token(token)
        assert result == '""'

    def test_format_number_integer(self):
        """Test formatting integer number."""
        token = Token(TokenType.TK_NUMBER, 42.0, line=1)
        result = Detokenizer.format_token(token)
        assert result == "42.0"

    def test_format_number_decimal(self):
        """Test formatting decimal number."""
        token = Token(TokenType.TK_NUMBER, 3.14, line=1)
        result = Detokenizer.format_token(token)
        assert result == "3.14"

    def test_format_number_scientific(self):
        """Test formatting number in scientific notation."""
        token = Token(TokenType.TK_NUMBER, 1.5e-3, line=1)
        result = Detokenizer.format_token(token)
        # Small numbers will display with 'e' notation
        assert "e" in result.lower() or result == "0.0015"

    def test_format_identifier(self):
        """Test formatting identifier (TK_NAME)."""
        token = Token(TokenType.TK_NAME, "myvar", line=1)
        result = Detokenizer.format_token(token)
        assert result == "myvar"

    def test_format_unicode_identifier(self):
        """Test formatting Unicode identifier."""
        token = Token(TokenType.TK_NAME, "变量", line=1)
        result = Detokenizer.format_token(token)
        assert result == "变量"

    def test_format_single_char_operators(self):
        """Test formatting single character tokens."""
        chars = "(){}[];,.+-*/"
        for char in chars:
            token = Token(ord(char), line=1)
            result = Detokenizer.format_token(token)
            assert result == char

    def test_format_concat_operator(self):
        """Test formatting concat operator (..)."""
        token = Token(TokenType.TK_CONCAT, line=1)
        result = Detokenizer.format_token(token)
        assert result == ".."

    def test_format_dots_operator(self):
        """Test formatting dots operator (...)."""
        token = Token(TokenType.TK_DOTS, line=1)
        result = Detokenizer.format_token(token)
        assert result == "..."

    def test_format_equality_operators(self):
        """Test formatting comparison operators."""
        operators = [
            (TokenType.TK_EQ, "=="),
            (TokenType.TK_GE, ">="),
            (TokenType.TK_LE, "<="),
            (TokenType.TK_NE, "~="),
        ]

        for token_type, expected in operators:
            token = Token(token_type, line=1)
            result = Detokenizer.format_token(token)
            assert result == expected

    def test_format_eos_token(self):
        """Test formatting EOS token (should return empty string)."""
        token = Token(TokenType.TK_EOS, line=1)
        result = Detokenizer.format_token(token)
        assert result == ""

    def test_format_token_default_language(self):
        """Test that default language is English."""
        token = Token(TokenType.TK_IF, line=1)
        result = Detokenizer.format_token(token)  # No language specified
        assert result == "if"


class TestDetokenize:
    """Tests for detokenize() function."""

    def test_translate_simple_expression(self):
        """Test translating simple expression."""
        tokens = [
            Token(TokenType.TK_NAME, "x", line=1),
            Token(ord('+'), line=1),
            Token(TokenType.TK_NUMBER, 1.0, line=1),
            Token(TokenType.TK_EOS, line=1),
        ]
        result = Detokenizer.detokenize(tokens, target_language='english')
        assert result == "x + 1.0"

    def test_translate_with_keywords_to_english(self):
        """Test translating keywords to English."""
        tokens = [
            Token(TokenType.TK_IF, line=1),
            Token(TokenType.TK_NAME, "x", line=1),
            Token(TokenType.TK_THEN, line=1),
            Token(TokenType.TK_RETURN, line=1),
            Token(TokenType.TK_NAME, "y", line=1),
            Token(TokenType.TK_END, line=1),
            Token(TokenType.TK_EOS, line=1),
        ]
        result = Detokenizer.detokenize(tokens, target_language='english')
        assert result == "if x then return y end"

    def test_translate_with_keywords_to_spanish(self):
        """Test translating keywords to Spanish with conflict resolution."""
        tokens = [
            Token(TokenType.TK_IF, line=1),
            Token(TokenType.TK_NAME, "x", line=1),
            Token(TokenType.TK_THEN, line=1),
            Token(TokenType.TK_RETURN, line=1),
            Token(TokenType.TK_NAME, "y", line=1),
            Token(TokenType.TK_END, line=1),
            Token(TokenType.TK_EOS, line=1),
        ]
        result = Detokenizer.detokenize(tokens, target_language='spanish')
        # Note: 'y' is renamed to '_y' because 'y' is Spanish keyword for AND
        assert result == "si x entonces devolver _y fin"

    def test_translate_with_keywords_to_mandarin(self):
        """Test translating keywords to Mandarin."""
        tokens = [
            Token(TokenType.TK_IF, line=1),
            Token(TokenType.TK_NAME, "x", line=1),
            Token(TokenType.TK_THEN, line=1),
            Token(TokenType.TK_END, line=1),
            Token(TokenType.TK_EOS, line=1),
        ]
        result = Detokenizer.detokenize(tokens, target_language='mandarin')
        assert result == "如果 x 那么 结束"

    def test_translate_with_strings(self):
        """Test translating tokens with string literals."""
        tokens = [
            Token(TokenType.TK_NAME, "print", line=1),
            Token(ord('('), line=1),
            Token(TokenType.TK_STRING, "hello", line=1),
            Token(ord(')'), line=1),
            Token(TokenType.TK_EOS, line=1),
        ]
        result = Detokenizer.detokenize(tokens)
        assert result == 'print("hello")'

    def test_translate_with_numbers(self):
        """Test translating tokens with numbers."""
        tokens = [
            Token(TokenType.TK_NAME, "x", line=1),
            Token(ord('='), line=1),
            Token(TokenType.TK_NUMBER, 42.0, line=1),
            Token(TokenType.TK_EOS, line=1),
        ]
        result = Detokenizer.detokenize(tokens)
        assert result == "x = 42.0"

    def test_translate_with_operators(self):
        """Test translating with various operators."""
        tokens = [
            Token(TokenType.TK_NAME, "a", line=1),
            Token(TokenType.TK_CONCAT, line=1),
            Token(TokenType.TK_NAME, "b", line=1),
            Token(TokenType.TK_EOS, line=1),
        ]
        result = Detokenizer.detokenize(tokens)
        assert result == "a .. b"

    def test_translate_comparison_operators(self):
        """Test translating comparison operators."""
        tokens = [
            Token(TokenType.TK_NAME, "x", line=1),
            Token(TokenType.TK_EQ, line=1),
            Token(TokenType.TK_NUMBER, 5.0, line=1),
            Token(TokenType.TK_EOS, line=1),
        ]
        result = Detokenizer.detokenize(tokens)
        assert result == "x == 5.0"

    def test_translate_empty_token_list(self):
        """Test translating empty token list."""
        tokens = [Token(TokenType.TK_EOS, line=1)]
        result = Detokenizer.detokenize(tokens)
        assert result == ""

    def test_translate_only_eos_skipped(self):
        """Test that only EOS tokens produce empty output."""
        tokens = [
            Token(TokenType.TK_NAME, "x", line=1),
            Token(TokenType.TK_EOS, line=1),
        ]
        result = Detokenizer.detokenize(tokens)
        assert result == "x"

    def test_translate_complex_expression(self):
        """Test translating complex expression."""
        tokens = [
            Token(TokenType.TK_LOCAL, line=1),
            Token(TokenType.TK_FUNCTION, line=1),
            Token(TokenType.TK_NAME, "test", line=1),
            Token(ord('('), line=1),
            Token(TokenType.TK_NAME, "n", line=1),
            Token(ord(')'), line=1),
            Token(TokenType.TK_RETURN, line=1),
            Token(TokenType.TK_NAME, "n", line=1),
            Token(ord('*'), line=1),
            Token(TokenType.TK_NUMBER, 2.0, line=1),
            Token(TokenType.TK_END, line=1),
            Token(TokenType.TK_EOS, line=1),
        ]
        result = Detokenizer.detokenize(tokens, target_language='english')
        assert "local" in result
        assert "function" in result
        assert "return" in result
        assert "end" in result

    def test_translate_with_dots(self):
        """Test translating with dots (vararg)."""
        tokens = [
            Token(TokenType.TK_FUNCTION, line=1),
            Token(TokenType.TK_NAME, "f", line=1),
            Token(ord('('), line=1),
            Token(TokenType.TK_DOTS, line=1),
            Token(ord(')'), line=1),
            Token(TokenType.TK_END, line=1),
            Token(TokenType.TK_EOS, line=1),
        ]
        result = Detokenizer.detokenize(tokens)
        assert "..." in result

    def test_translate_preserves_identifier_names(self):
        """Test that identifier names are preserved during translation."""
        tokens = [
            Token(TokenType.TK_LOCAL, line=1),
            Token(TokenType.TK_NAME, "myVariable123", line=1),
            Token(TokenType.TK_EOS, line=1),
        ]
        result = Detokenizer.detokenize(tokens)
        assert "myVariable123" in result

    def test_translate_unicode_identifiers(self):
        """Test translating with Unicode identifiers."""
        tokens = [
            Token(TokenType.TK_LOCAL, line=1),
            Token(TokenType.TK_NAME, "变量", line=1),
            Token(TokenType.TK_EOS, line=1),
        ]
        result = Detokenizer.detokenize(tokens)
        assert "变量" in result


class TestDetokenizeEnglish:
    """Tests for detokenizing to English."""

    def test_translate_to_english_simple(self):
        """Test detokenizing to English."""
        tokens = [
            Token(TokenType.TK_IF, line=1),
            Token(TokenType.TK_NAME, "x", line=1),
            Token(TokenType.TK_THEN, line=1),
            Token(TokenType.TK_END, line=1),
            Token(TokenType.TK_EOS, line=1),
        ]
        result = Detokenizer.detokenize(tokens, target_language='english')
        assert result == "if x then end"

    def test_translate_to_english_matches_default(self):
        """Test that explicit English matches default detokenize."""
        tokens = [
            Token(TokenType.TK_FUNCTION, line=1),
            Token(TokenType.TK_NAME, "test", line=1),
            Token(ord('('), line=1),
            Token(ord(')'), line=1),
            Token(TokenType.TK_END, line=1),
            Token(TokenType.TK_EOS, line=1),
        ]

        result1 = Detokenizer.detokenize(tokens, target_language='english')
        result2 = Detokenizer.detokenize(tokens)  # Default is English
        assert result1 == result2

    def test_translate_to_english_complex(self):
        """Test detokenizing complex token stream to English."""
        tokens = [
            Token(TokenType.TK_LOCAL, line=1),
            Token(TokenType.TK_FUNCTION, line=1),
            Token(TokenType.TK_NAME, "factorial", line=1),
            Token(ord('('), line=1),
            Token(TokenType.TK_NAME, "n", line=1),
            Token(ord(')'), line=1),
            Token(TokenType.TK_IF, line=2),
            Token(TokenType.TK_NAME, "n", line=2),
            Token(TokenType.TK_LE, line=2),
            Token(TokenType.TK_NUMBER, 1.0, line=2),
            Token(TokenType.TK_THEN, line=2),
            Token(TokenType.TK_RETURN, line=3),
            Token(TokenType.TK_NUMBER, 1.0, line=3),
            Token(TokenType.TK_ELSE, line=4),
            Token(TokenType.TK_RETURN, line=5),
            Token(TokenType.TK_NAME, "n", line=5),
            Token(ord('*'), line=5),
            Token(TokenType.TK_NAME, "factorial", line=5),
            Token(ord('('), line=5),
            Token(TokenType.TK_NAME, "n", line=5),
            Token(ord('-'), line=5),
            Token(TokenType.TK_NUMBER, 1.0, line=5),
            Token(ord(')'), line=5),
            Token(TokenType.TK_END, line=6),
            Token(TokenType.TK_END, line=7),
            Token(TokenType.TK_EOS, line=7),
        ]

        result = Detokenizer.detokenize(tokens, target_language='english')
        assert "local function factorial" in result
        assert "if n <= 1.0 then" in result
        assert "return 1.0" in result
        assert "else" in result
        assert "end" in result


class TestEdgeCases:
    """Tests for edge cases and special scenarios."""

    def test_format_token_with_none_value(self):
        """Test formatting token with None value (keywords)."""
        token = Token(TokenType.TK_IF, value=None, line=1)
        result = Detokenizer.format_token(token)
        assert result == "if"

    def test_translate_single_token(self):
        """Test translating single token."""
        tokens = [Token(TokenType.TK_NAME, "x", line=1)]
        result = Detokenizer.detokenize(tokens)
        assert result == "x"

    def test_translate_all_operator_types(self):
        """Test translating all multi-char operator types."""
        tokens = [
            Token(TokenType.TK_CONCAT, line=1),  # ..
            Token(TokenType.TK_DOTS, line=1),    # ...
            Token(TokenType.TK_EQ, line=1),      # ==
            Token(TokenType.TK_GE, line=1),      # >=
            Token(TokenType.TK_LE, line=1),      # <=
            Token(TokenType.TK_NE, line=1),      # ~=
            Token(TokenType.TK_EOS, line=1),
        ]
        result = Detokenizer.detokenize(tokens)
        assert result == ".. ... == >= <= ~="

    def test_format_token_special_characters_in_string(self):
        """Test formatting string with special characters."""
        token = Token(TokenType.TK_STRING, "hello\nworld\ttab", line=1)
        result = Detokenizer.format_token(token)
        assert '"hello\nworld\ttab"' == result

    def test_translate_mixed_languages_identifiers(self):
        """Test that identifiers remain unchanged regardless of target language."""
        tokens = [
            Token(TokenType.TK_NAME, "englishVar", line=1),
            Token(TokenType.TK_NAME, "变量中文", line=1),
            Token(TokenType.TK_NAME, "españolVar", line=1),
            Token(TokenType.TK_EOS, line=1),
        ]

        # Test all target languages preserve identifiers
        for lang in ['english', 'spanish', 'mandarin']:
            result = Detokenizer.detokenize(tokens, target_language=lang)
            assert "englishVar" in result
            assert "变量中文" in result
            assert "españolVar" in result

    def test_translate_large_number_of_tokens(self):
        """Test translating large number of tokens."""
        tokens = []
        for i in range(100):
            tokens.append(Token(TokenType.TK_NAME, f"var{i}", line=1))
            tokens.append(Token(ord('+'), line=1))
        tokens.append(Token(TokenType.TK_EOS, line=1))

        result = Detokenizer.detokenize(tokens)
        assert len(result) > 0
        assert "var0" in result
        assert "var99" in result


class TestIdentifierConflictResolution:
    """Tests for cross-language identifier conflict resolution."""

    def test_identifier_conflicts_with_keyword(self):
        """Test that identifier conflicting with target keyword is renamed."""
        tokens = [
            Token(TokenType.TK_NAME, "y", line=1),
            Token(TokenType.TK_EOS, line=1),
        ]
        result = Detokenizer.detokenize(tokens, target_language='spanish')
        assert result == "_y"

    def test_multiple_identifier_conflicts(self):
        """Test multiple identifiers conflicting with keywords."""
        tokens = [
            Token(TokenType.TK_NAME, "y", line=1),
            Token(TokenType.TK_NAME, "o", line=1),
            Token(TokenType.TK_NAME, "si", line=1),
            Token(TokenType.TK_EOS, line=1),
        ]
        result = Detokenizer.detokenize(tokens, target_language='spanish')
        assert "_y" in result
        assert "_o" in result
        assert "_si" in result

    def test_conflict_resolution_consistent(self):
        """Test that conflicting identifier is renamed consistently."""
        tokens = [
            Token(TokenType.TK_LOCAL, line=1),
            Token(TokenType.TK_NAME, "y", line=1),
            Token(ord('='), line=1),
            Token(TokenType.TK_NUMBER, 5.0, line=1),
            Token(TokenType.TK_RETURN, line=2),
            Token(TokenType.TK_NAME, "y", line=2),
            Token(TokenType.TK_EOS, line=2),
        ]
        result = Detokenizer.detokenize(tokens, target_language='spanish')
        assert result.count("_y") == 2

    def test_no_conflicts_unchanged(self):
        """Test that identifiers with no conflicts remain unchanged."""
        tokens = [
            Token(TokenType.TK_NAME, "myVariable", line=1),
            Token(TokenType.TK_NAME, "x", line=1),
            Token(TokenType.TK_EOS, line=1),
        ]
        result = Detokenizer.detokenize(tokens, target_language='spanish')
        assert "myVariable" in result
        assert "x" in result

    def test_nested_conflict_resolution(self):
        """Test conflict where renamed identifier also exists."""
        tokens = [
            Token(TokenType.TK_NAME, "y", line=1),
            Token(TokenType.TK_NAME, "_y", line=1),
            Token(TokenType.TK_EOS, line=1),
        ]
        result = Detokenizer.detokenize(tokens, target_language='spanish')
        assert "__y" in result
        assert "_y" in result

    def test_english_to_spanish_with_conflict(self):
        """Test full English to Spanish translation with identifier conflict."""
        tokens = [
            Token(TokenType.TK_IF, line=1),
            Token(TokenType.TK_NAME, "y", line=1),
            Token(TokenType.TK_THEN, line=1),
            Token(TokenType.TK_RETURN, line=2),
            Token(TokenType.TK_NAME, "y", line=2),
            Token(TokenType.TK_END, line=3),
            Token(TokenType.TK_EOS, line=3),
        ]
        result = Detokenizer.detokenize(tokens, target_language='spanish')
        assert "si _y" in result
        assert "devolver _y" in result

    def test_unicode_identifier_conflict(self):
        """Test conflict with Unicode characters in target language."""
        tokens = [
            Token(TokenType.TK_NAME, "和", line=1),
            Token(TokenType.TK_EOS, line=1),
        ]
        result = Detokenizer.detokenize(tokens, target_language='mandarin')
        assert result == "_和"

    def test_detokenize_backward_compatible(self):
        """Test that detokenize without conflicts works as before."""
        tokens = [
            Token(TokenType.TK_FUNCTION, line=1),
            Token(TokenType.TK_NAME, "test", line=1),
            Token(ord('('), line=1),
            Token(ord(')'), line=1),
            Token(TokenType.TK_END, line=1),
            Token(TokenType.TK_EOS, line=1),
        ]

        # English to English should work exactly as before
        result = Detokenizer.detokenize(tokens, target_language='english')
        assert result == "function test() end"

    def test_all_identifiers_conflict(self):
        """Test when every identifier conflicts with target keywords."""
        tokens = [
            Token(TokenType.TK_NAME, "y", line=1),
            Token(TokenType.TK_NAME, "o", line=1),
            Token(TokenType.TK_NAME, "si", line=1),
            Token(TokenType.TK_NAME, "no", line=1),
            Token(TokenType.TK_EOS, line=1),
        ]
        result = Detokenizer.detokenize(tokens, target_language='spanish')
        assert result == "_y _o _si _no"

    def test_conflict_resolution_empty_tokens(self):
        """Test conflict resolution with empty token list."""
        tokens = [Token(TokenType.TK_EOS, line=1)]
        result = Detokenizer.detokenize(tokens, target_language='spanish')
        assert result == ""