"""
Comprehensive tests for Tokenizer class.
Tests all tokenization methods including read_name, read_number, read_string, etc.
"""

import pytest
from multilang_lexer.lexer_state import LexerState
from multilang_lexer.tokenizer import Tokenizer
from multilang_lexer.tokens import Token, TokenType
from multilang_lexer.exceptions import LexerError


class TestReadName:
    """Tests for Tokenizer.read_name() method."""

    def test_simple_identifier(self):
        """Test reading simple ASCII identifier."""
        state = LexerState("hello world")
        name = Tokenizer.read_name(state)
        assert name == "hello"
        assert state.current == ' '  # Stopped at space

    def test_identifier_with_underscore(self):
        """Test identifier with underscores."""
        state = LexerState("_private_var")
        name = Tokenizer.read_name(state)
        assert name == "_private_var"

    def test_identifier_with_numbers(self):
        """Test identifier with numbers."""
        state = LexerState("var123 ")
        name = Tokenizer.read_name(state)
        assert name == "var123"

    def test_identifier_starting_with_number_not_called(self):
        """Test that read_name reads alphanumeric characters."""
        # read_name will read the entire "123var" since isalnum() passes for digits too
        # This is expected - lex_next_token routes to read_number first for digit starts
        state = LexerState("123var")
        name = Tokenizer.read_name(state)
        assert name == "123var"  # read_name doesn't care about leading digits

    def test_unicode_identifier(self):
        """Test Unicode identifier (e.g., Chinese)."""
        state = LexerState("函数名称 ")
        name = Tokenizer.read_name(state)
        assert name == "函数名称"

    def test_mixed_unicode_ascii(self):
        """Test mixed Unicode and ASCII."""
        state = LexerState("test函数123_var")
        name = Tokenizer.read_name(state)
        assert name == "test函数123_var"

    def test_identifier_at_end_of_source(self):
        """Test identifier at end of source."""
        state = LexerState("identifier")
        name = Tokenizer.read_name(state)
        assert name == "identifier"
        assert state.current == ''  # EOZ


class TestReadNumber:
    """Tests for Tokenizer.read_number() method."""

    def test_simple_integer(self):
        """Test reading simple integer."""
        state = LexerState("42 ")
        num = Tokenizer.read_number(state)
        assert num == 42.0
        assert state.current == ' '

    def test_decimal_number(self):
        """Test reading decimal number."""
        state = LexerState("3.14")
        num = Tokenizer.read_number(state)
        assert num == 3.14

    def test_number_starting_with_dot(self):
        """Test number starting with decimal point."""
        state = LexerState("5 ")
        num = Tokenizer.read_number(state, starts_with_dot=True)
        assert num == 0.5

    def test_scientific_notation_lowercase_e(self):
        """Test scientific notation with lowercase e."""
        state = LexerState("1e10 ")
        num = Tokenizer.read_number(state)
        assert num == 1e10

    def test_scientific_notation_uppercase_e(self):
        """Test scientific notation with uppercase E."""
        state = LexerState("2.5E-3 ")
        num = Tokenizer.read_number(state)
        assert num == 2.5e-3

    def test_scientific_notation_positive_exponent(self):
        """Test scientific notation with explicit positive sign."""
        state = LexerState("1.5e+5 ")
        num = Tokenizer.read_number(state)
        assert num == 1.5e5

    def test_zero(self):
        """Test reading zero."""
        state = LexerState("0 ")
        num = Tokenizer.read_number(state)
        assert num == 0.0

    def test_decimal_without_integer_part(self):
        """Test decimal starting with dot."""
        state = LexerState("123 ")
        num = Tokenizer.read_number(state, starts_with_dot=True)
        assert num == 0.123

    def test_number_with_trailing_zeros(self):
        """Test number with trailing zeros."""
        state = LexerState("100.00 ")
        num = Tokenizer.read_number(state)
        assert num == 100.0

    def test_ambiguous_decimal_concat_error(self):
        """Test error on ambiguous decimal/concat syntax."""
        state = LexerState("3... ")
        state._next()  # Move past '3'
        state._save('3')
        state._clear_buffer()

        with pytest.raises(LexerError) as exc_info:
            Tokenizer.read_number(state)
        assert "ambiguous syntax" in str(exc_info.value)

    def test_very_large_number(self):
        """Test very large number."""
        state = LexerState("999999999999999999 ")
        num = Tokenizer.read_number(state)
        assert num == 999999999999999999

    def test_very_small_number(self):
        """Test very small decimal."""
        state = LexerState("0.000001 ")
        num = Tokenizer.read_number(state)
        assert num == 0.000001


class TestReadString:
    """Tests for Tokenizer.read_string() method."""

    def test_simple_double_quoted_string(self):
        """Test simple double-quoted string."""
        state = LexerState('"hello"')
        s = Tokenizer.read_string(state, '"')
        assert s == "hello"

    def test_simple_single_quoted_string(self):
        """Test simple single-quoted string."""
        state = LexerState("'world'")
        s = Tokenizer.read_string(state, "'")
        assert s == "world"

    def test_string_with_spaces(self):
        """Test string containing spaces."""
        state = LexerState('"hello world"')
        s = Tokenizer.read_string(state, '"')
        assert s == "hello world"

    def test_empty_string(self):
        """Test empty string."""
        state = LexerState('""')
        s = Tokenizer.read_string(state, '"')
        assert s == ""

    def test_string_with_escape_sequences(self):
        """Test common escape sequences."""
        state = LexerState(r'"hello\nworld"')
        s = Tokenizer.read_string(state, '"')
        assert s == "hello\nworld"

    def test_escape_tab(self):
        """Test tab escape."""
        state = LexerState(r'"\t"')
        s = Tokenizer.read_string(state, '"')
        assert s == "\t"

    def test_escape_backslash(self):
        """Test backslash escape."""
        state = LexerState(r'"\\"')
        s = Tokenizer.read_string(state, '"')
        assert s == "\\"

    def test_escape_quote(self):
        """Test escaped quote."""
        state = LexerState(r'"say \"hi\""')
        s = Tokenizer.read_string(state, '"')
        assert s == 'say "hi"'

    def test_numeric_escape_decimal(self):
        """Test numeric escape sequence."""
        state = LexerState(r'"\065"')  # 'A' in decimal
        s = Tokenizer.read_string(state, '"')
        assert s == "A"

    def test_numeric_escape_three_digits(self):
        """Test 3-digit numeric escape."""
        state = LexerState(r'"\097"')  # 'a' in decimal
        s = Tokenizer.read_string(state, '"')
        assert s == "a"

    def test_numeric_escape_too_large(self):
        """Test that numeric escape > 255 raises error."""
        state = LexerState(r'"\999"')
        with pytest.raises(LexerError) as exc_info:
            Tokenizer.read_string(state, '"')
        assert "escape sequence too large" in str(exc_info.value)

    def test_escape_newline_literal(self):
        """Test escaped newline (continuation)."""
        state = LexerState('"\\\nworld"')
        s = Tokenizer.read_string(state, '"')
        assert s == "\nworld"

    def test_unknown_escape(self):
        """Test unknown escape sequence (should just save character)."""
        state = LexerState(r'"\x"')
        s = Tokenizer.read_string(state, '"')
        assert s == "x"

    def test_unfinished_string(self):
        """Test error on unfinished string."""
        state = LexerState('"hello')
        with pytest.raises(LexerError) as exc_info:
            Tokenizer.read_string(state, '"')
        assert "unfinished string" in str(exc_info.value)

    def test_string_with_newline_error(self):
        """Test that unescaped newline in string raises error."""
        state = LexerState('"hello\nworld"')
        with pytest.raises(LexerError) as exc_info:
            Tokenizer.read_string(state, '"')
        assert "unfinished string" in str(exc_info.value)

    def test_string_with_unicode(self):
        """Test string containing Unicode."""
        state = LexerState('"函数"')
        s = Tokenizer.read_string(state, '"')
        assert s == "函数"


class TestReadLongString:
    """Tests for Tokenizer.read_long_string() method."""

    def test_simple_long_string(self):
        """Test simple long string."""
        state = LexerState("[[hello]]")
        state._next()  # Skip first '['
        s = Tokenizer.read_long_string(state)
        assert s == "hello"

    def test_long_string_with_newlines(self):
        """Test long string with newlines."""
        state = LexerState("[[line1\nline2\nline3]]")
        state._next()
        s = Tokenizer.read_long_string(state)
        assert s == "line1\nline2\nline3"

    def test_long_string_with_single_bracket(self):
        """Test long string containing single bracket."""
        state = LexerState("[[hello[world]]")
        state._next()
        s = Tokenizer.read_long_string(state)
        assert s == "hello[world"

    def test_nested_long_string(self):
        """Test nested long string brackets."""
        state = LexerState("[[outer [[inner]] outer]]")
        state._next()
        s = Tokenizer.read_long_string(state)
        assert s == "outer [[inner]] outer"

    def test_multiple_nesting_levels(self):
        """Test multiple nesting levels."""
        state = LexerState("[[a [[b [[c]] b]] a]]")
        state._next()
        s = Tokenizer.read_long_string(state)
        assert s == "a [[b [[c]] b]] a"

    def test_unfinished_long_string(self):
        """Test error on unfinished long string."""
        state = LexerState("[[hello")
        state._next()
        with pytest.raises(LexerError) as exc_info:
            Tokenizer.read_long_string(state)
        assert "unfinished long string" in str(exc_info.value)

    def test_long_string_empty(self):
        """Test empty long string."""
        state = LexerState("[[]]")
        state._next()
        s = Tokenizer.read_long_string(state)
        assert s == ""

    def test_long_string_with_close_bracket_at_end(self):
        """Test long string with extra ] after closing ]]."""
        # [[test]] closes the string, the extra ] is left in stream
        state = LexerState("[[test]]")
        state._next()
        s = Tokenizer.read_long_string(state)
        assert s == "test"


class TestLexNextToken:
    """Tests for Tokenizer.lex_next_token() method."""

    def test_whitespace_skipped(self):
        """Test that whitespace is skipped."""
        state = LexerState("   \t  x")
        token = Tokenizer.lex_next_token(state)
        assert token.type == TokenType.TK_NAME
        assert token.value == "x"

    def test_newlines_skipped(self):
        """Test that newlines are skipped and line number incremented."""
        state = LexerState("\n\nx")
        token = Tokenizer.lex_next_token(state)
        assert token.type == TokenType.TK_NAME
        assert token.line == 3

    def test_end_of_source(self):
        """Test TK_EOS at end of source."""
        state = LexerState("")
        token = Tokenizer.lex_next_token(state)
        assert token.type == TokenType.TK_EOS

    def test_dollar_sign_error(self):
        """Test that dollar sign raises error."""
        state = LexerState("$")
        with pytest.raises(LexerError) as exc_info:
            Tokenizer.lex_next_token(state)
        assert "pragmas are no longer supported" in str(exc_info.value)

    def test_minus_operator(self):
        """Test minus as operator."""
        state = LexerState("- ")
        token = Tokenizer.lex_next_token(state)
        assert token.type == ord('-')

    def test_comment_single_line(self):
        """Test single-line comment."""
        state = LexerState("-- this is a comment\nx")
        token = Tokenizer.lex_next_token(state)
        assert token.type == TokenType.TK_NAME
        assert token.value == "x"

    def test_comment_at_end_of_file(self):
        """Test comment at end of file."""
        state = LexerState("-- comment")
        token = Tokenizer.lex_next_token(state)
        assert token.type == TokenType.TK_EOS

    def test_long_string_token(self):
        """Test long string creates TK_STRING token."""
        state = LexerState("[[hello]]")
        token = Tokenizer.lex_next_token(state)
        assert token.type == TokenType.TK_STRING
        assert token.value == "hello"

    def test_left_bracket_not_long_string(self):
        """Test single left bracket."""
        state = LexerState("[ ")
        token = Tokenizer.lex_next_token(state)
        assert token.type == ord('[')

    def test_equality_operator(self):
        """Test == operator."""
        state = LexerState("==")
        token = Tokenizer.lex_next_token(state)
        assert token.type == TokenType.TK_EQ

    def test_single_equals(self):
        """Test single = (assignment)."""
        state = LexerState("= ")
        token = Tokenizer.lex_next_token(state)
        assert token.type == ord('=')

    def test_less_than_or_equal(self):
        """Test <= operator."""
        state = LexerState("<=")
        token = Tokenizer.lex_next_token(state)
        assert token.type == TokenType.TK_LE

    def test_less_than(self):
        """Test < operator."""
        state = LexerState("< ")
        token = Tokenizer.lex_next_token(state)
        assert token.type == ord('<')

    def test_greater_than_or_equal(self):
        """Test >= operator."""
        state = LexerState(">=")
        token = Tokenizer.lex_next_token(state)
        assert token.type == TokenType.TK_GE

    def test_greater_than(self):
        """Test > operator."""
        state = LexerState("> ")
        token = Tokenizer.lex_next_token(state)
        assert token.type == ord('>')

    def test_not_equal(self):
        """Test ~= operator."""
        state = LexerState("~=")
        token = Tokenizer.lex_next_token(state)
        assert token.type == TokenType.TK_NE

    def test_tilde_alone(self):
        """Test ~ alone."""
        state = LexerState("~ ")
        token = Tokenizer.lex_next_token(state)
        assert token.type == ord('~')

    def test_string_double_quote(self):
        """Test double-quoted string."""
        state = LexerState('"test"')
        token = Tokenizer.lex_next_token(state)
        assert token.type == TokenType.TK_STRING
        assert token.value == "test"

    def test_string_single_quote(self):
        """Test single-quoted string."""
        state = LexerState("'test'")
        token = Tokenizer.lex_next_token(state)
        assert token.type == TokenType.TK_STRING
        assert token.value == "test"

    def test_concat_operator(self):
        """Test .. (concat) operator."""
        state = LexerState("..")
        token = Tokenizer.lex_next_token(state)
        assert token.type == TokenType.TK_CONCAT

    def test_dots_vararg(self):
        """Test ... (dots) token."""
        state = LexerState("...")
        token = Tokenizer.lex_next_token(state)
        assert token.type == TokenType.TK_DOTS

    def test_single_dot(self):
        """Test single . (field access)."""
        state = LexerState(". ")
        token = Tokenizer.lex_next_token(state)
        assert token.type == ord('.')

    def test_number_starting_with_dot(self):
        """Test number starting with decimal point."""
        state = LexerState(".5")
        token = Tokenizer.lex_next_token(state)
        assert token.type == TokenType.TK_NUMBER
        assert token.value == 0.5

    def test_integer_number(self):
        """Test integer number."""
        state = LexerState("42")
        token = Tokenizer.lex_next_token(state)
        assert token.type == TokenType.TK_NUMBER
        assert token.value == 42.0

    def test_english_keyword(self):
        """Test English keyword recognition."""
        state = LexerState("function", language="english")
        token = Tokenizer.lex_next_token(state)
        assert token.type == TokenType.TK_FUNCTION
        assert token.value is None

    def test_spanish_keyword(self):
        """Test Spanish keyword recognition."""
        state = LexerState("función", language="spanish")
        token = Tokenizer.lex_next_token(state)
        assert token.type == TokenType.TK_FUNCTION

    def test_mandarin_keyword(self):
        """Test Mandarin keyword recognition."""
        state = LexerState("函数", language="mandarin")
        token = Tokenizer.lex_next_token(state)
        assert token.type == TokenType.TK_FUNCTION

    def test_identifier_not_keyword(self):
        """Test identifier that is not a keyword."""
        state = LexerState("myvar")
        token = Tokenizer.lex_next_token(state)
        assert token.type == TokenType.TK_NAME
        assert token.value == "myvar"

    def test_control_character_error(self):
        """Test that control characters raise error."""
        state = LexerState("\x01")  # SOH control character
        with pytest.raises(LexerError) as exc_info:
            Tokenizer.lex_next_token(state)
        assert "invalid control char" in str(exc_info.value)

    def test_single_char_operator(self):
        """Test single character operators."""
        for char in "(){}[];,*+/-":
            state = LexerState(char)
            token = Tokenizer.lex_next_token(state)
            assert token.type == ord(char)


class TestTokenizeAll:
    """Tests for Tokenizer.tokenize_all() method."""

    def test_tokenize_empty_source(self):
        """Test tokenizing empty source."""
        state = LexerState("")
        tokens = Tokenizer.tokenize_all(state)
        assert len(tokens) == 1
        assert tokens[0].type == TokenType.TK_EOS

    def test_tokenize_simple_expression(self):
        """Test tokenizing simple expression."""
        state = LexerState("x + 1")
        tokens = Tokenizer.tokenize_all(state)
        assert len(tokens) == 4  # x, +, 1, EOS
        assert tokens[0].type == TokenType.TK_NAME
        assert tokens[1].type == ord('+')
        assert tokens[2].type == TokenType.TK_NUMBER
        assert tokens[3].type == TokenType.TK_EOS

    def test_tokenize_includes_eos(self):
        """Test that tokenize_all includes EOS token."""
        state = LexerState("test")
        tokens = Tokenizer.tokenize_all(state)
        assert tokens[-1].type == TokenType.TK_EOS

    def test_tokenize_with_comments(self):
        """Test that comments are skipped during tokenization."""
        state = LexerState("x -- comment\ny")
        tokens = Tokenizer.tokenize_all(state)
        names = [t for t in tokens if t.type == TokenType.TK_NAME]
        assert len(names) == 2
        assert names[0].value == "x"
        assert names[1].value == "y"

    def test_tokenize_complex_code(self):
        """Test tokenizing complex code."""
        code = """
        function factorial(n)
            if n <= 1 then
                return 1
            end
        end
        """
        state = LexerState(code, language="english")
        tokens = Tokenizer.tokenize_all(state)
        # Should have multiple tokens including keywords, identifiers, numbers
        assert len(tokens) > 10
        assert tokens[-1].type == TokenType.TK_EOS