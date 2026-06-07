"""
Comprehensive tests for LexerState class.
Tests state management, character traversal, buffering, and error handling.
"""

import pytest
from multilang_lexer.lexer_state import LexerState
from multilang_lexer.exceptions import LexerError
from multilang_lexer.tokens import TokenType


class TestLexerStateInitialization:
    """Tests for LexerState initialization."""

    def test_basic_initialization(self):
        """Test basic state initialization."""
        state = LexerState("hello world", "<test>", "english")
        assert state.source == "hello world"
        assert state.source_name == "<test>"
        assert state.language == "english"
        assert state.pos == 1  # Should advance to first char
        assert state.current == 'h'  # First character
        assert state.linenumber == 1
        assert state.buffer == []

    def test_default_parameters(self):
        """Test default parameter values."""
        state = LexerState("test")
        assert state.source_name == "<input>"
        assert state.language == "english"

    def test_empty_source(self):
        """Test initialization with empty source."""
        state = LexerState("")
        assert state.current == ''  # EOZ
        assert state.pos == 0

    def test_reserved_words_built(self):
        """Test that reserved words dictionary is built correctly."""
        state = LexerState("test", language="english")
        assert "if" in state.reserved_words
        assert state.reserved_words["if"] == TokenType.TK_IF
        assert "function" in state.reserved_words
        assert state.reserved_words["function"] == TokenType.TK_FUNCTION

    def test_spanish_reserved_words(self):
        """Test reserved words for Spanish."""
        state = LexerState("test", language="spanish")
        assert "si" in state.reserved_words
        assert state.reserved_words["si"] == TokenType.TK_IF
        assert "función" in state.reserved_words
        assert state.reserved_words["función"] == TokenType.TK_FUNCTION

    def test_mandarin_reserved_words(self):
        """Test reserved words for Mandarin."""
        state = LexerState("test", language="mandarin")
        assert "如果" in state.reserved_words
        assert state.reserved_words["如果"] == TokenType.TK_IF
        assert "函数" in state.reserved_words
        assert state.reserved_words["函数"] == TokenType.TK_FUNCTION

    def test_shebang_skipped(self):
        """Test that shebang line is skipped during initialization."""
        state = LexerState("#!/usr/bin/env lua\nhello")
        assert state.current == '\n'  # Should stop at newline after skipping shebang
        assert state.linenumber == 1  # Still on line 1 (before crossing newline)

    def test_shebang_with_newline(self):
        """Test shebang followed by newline."""
        state = LexerState("#comment\ncode")
        assert state.current == '\n'


class TestCharacterNavigation:
    """Tests for character navigation methods."""

    def test_next_advances_position(self):
        """Test that _next() advances position correctly."""
        state = LexerState("abc")
        assert state.current == 'a'
        assert state.pos == 1

        state._next()
        assert state.current == 'b'
        assert state.pos == 2

        state._next()
        assert state.current == 'c'
        assert state.pos == 3

    def test_next_at_end_of_source(self):
        """Test _next() at end of source."""
        state = LexerState("a")
        assert state.current == 'a'

        state._next()
        assert state.current == ''  # EOZ
        assert state.pos == 1

        # Multiple calls should stay at EOZ
        state._next()
        assert state.current == ''

    def test_inclinenumber(self):
        """Test line number increment."""
        state = LexerState("a\nb\nc")
        assert state.linenumber == 1
        assert state.current == 'a'

        state._next()  # Move to '\n'
        assert state.current == '\n'

        state._inclinenumber()  # Should skip '\n' and increment line
        assert state.current == 'b'
        assert state.linenumber == 2

        state._next()  # Move to '\n'
        state._inclinenumber()
        assert state.current == 'c'
        assert state.linenumber == 3

    def test_save_and_next(self):
        """Test _save_and_next() method."""
        state = LexerState("abc")
        assert state.current == 'a'

        state._save_and_next()
        assert state.buffer == ['a']
        assert state.current == 'b'

        state._save_and_next()
        assert state.buffer == ['a', 'b']
        assert state.current == 'c'


class TestBufferOperations:
    """Tests for buffer management methods."""

    def test_save(self):
        """Test _save() adds to buffer."""
        state = LexerState("test")
        assert state.buffer == []

        state._save('x')
        assert state.buffer == ['x']

        state._save('y')
        assert state.buffer == ['x', 'y']

    def test_get_buffer(self):
        """Test _get_buffer() returns joined string."""
        state = LexerState("test")
        state._save('h')
        state._save('e')
        state._save('l')
        state._save('l')
        state._save('o')

        result = state._get_buffer()
        assert result == "hello"
        assert isinstance(result, str)

    def test_get_buffer_empty(self):
        """Test _get_buffer() on empty buffer."""
        state = LexerState("test")
        assert state._get_buffer() == ""

    def test_clear_buffer(self):
        """Test _clear_buffer() empties the buffer."""
        state = LexerState("test")
        state._save('a')
        state._save('b')
        assert len(state.buffer) == 2

        state._clear_buffer()
        assert state.buffer == []
        assert state._get_buffer() == ""

    def test_buffer_with_unicode(self):
        """Test buffer operations with Unicode characters."""
        state = LexerState("test")
        state._save('函')
        state._save('数')

        result = state._get_buffer()
        assert result == "函数"


class TestErrorHandling:
    """Tests for error handling."""

    def test_error_with_string_token(self):
        """Test error() with string token."""
        state = LexerState("test")
        with pytest.raises(LexerError) as exc_info:
            state.error("test error", "bad_token")

        assert "test error" in str(exc_info.value)
        assert "bad_token" in str(exc_info.value)
        assert "line 1" in str(exc_info.value)

    def test_error_with_token_type(self):
        """Test error() with TokenType."""
        state = LexerState("test")
        with pytest.raises(LexerError) as exc_info:
            state.error("number error", TokenType.TK_NUMBER)

        assert "number error" in str(exc_info.value)
        assert "<number>" in str(exc_info.value)

    def test_error_with_single_char_int(self):
        """Test error() with single character (int < 256)."""
        state = LexerState("test")
        with pytest.raises(LexerError) as exc_info:
            state.error("unexpected character", ord('$'))

        assert "unexpected character" in str(exc_info.value)
        assert "$" in str(exc_info.value)

    def test_error_with_reserved_token_int(self):
        """Test error() with reserved token (int >= 256)."""
        state = LexerState("test")
        with pytest.raises(LexerError) as exc_info:
            state.error("unexpected token", 257)  # TK_AND

        assert "unexpected token" in str(exc_info.value)

    def test_error_respects_line_number(self):
        """Test that error() uses current line number."""
        state = LexerState("a\nb\nc")
        state._next()  # Move to '\n'
        state._inclinenumber()  # Line 2
        state._next()  # Move to '\n'
        state._inclinenumber()  # Line 3

        with pytest.raises(LexerError) as exc_info:
            state.error("error on line 3", "token")

        assert "line 3" in str(exc_info.value)

    def test_error_without_token(self):
        """Test error() with default empty token."""
        state = LexerState("test")
        with pytest.raises(LexerError) as exc_info:
            state.error("generic error")

        assert "generic error" in str(exc_info.value)


class TestTranslations:
    """Tests for language translation loading."""

    def test_translations_loaded(self):
        """Test that translations are loaded correctly."""
        state = LexerState("test", language="english")
        assert state.translations is not None
        assert isinstance(state.translations, dict)
        assert state.translations['IF'] == 'if'

    def test_spanish_translations(self):
        """Test Spanish translations."""
        state = LexerState("test", language="spanish")
        assert state.translations['IF'] == 'si'
        assert state.translations['FUNCTION'] == 'función'

    def test_invalid_language(self):
        """Test that invalid language raises error."""
        with pytest.raises(FileNotFoundError):
            LexerState("test", language="invalid_language")


class TestEdgeCases:
    """Tests for edge cases and boundary conditions."""

    def test_single_character_source(self):
        """Test with single character source."""
        state = LexerState("x")
        assert state.current == 'x'
        state._next()
        assert state.current == ''

    def test_very_long_source(self):
        """Test with very long source."""
        long_source = "a" * 10000
        state = LexerState(long_source)
        assert state.current == 'a'
        assert len(state.source) == 10000

    def test_unicode_source(self):
        """Test with Unicode source."""
        state = LexerState("函数 测试")
        assert state.current == '函'
        state._next()
        assert state.current == '数'

    def test_special_characters(self):
        """Test with special characters."""
        state = LexerState("!@#$%^&*()")
        assert state.current == '!'
        state._next()
        assert state.current == '@'

    def test_whitespace_only(self):
        """Test with whitespace-only source."""
        state = LexerState("   \t\n  ")
        assert state.current == ' '

    def test_newline_characters(self):
        """Test different newline characters."""
        state = LexerState("a\nb\rc\r\nd")
        assert state.current == 'a'
        state._next()
        assert state.current == '\n'
        state._next()
        assert state.current == 'b'