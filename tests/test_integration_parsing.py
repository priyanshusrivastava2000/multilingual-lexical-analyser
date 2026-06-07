"""
Integration tests for parsing features.
Tests comments, whitespace, shebang, and line number tracking.
"""

import pytest
from multilang_lexer import Lexer, TokenType


class TestComments:
    """Test comment handling."""

    def test_single_line_comment(self):
        """Test single-line comments."""
        code = "x = 1 -- this is a comment"
        lexer = Lexer(code, language='english')
        tokens = lexer.tokenize()
        # Comments should be ignored
        names = [t for t in tokens if t.type == TokenType.TK_NAME]
        assert len(names) == 1
        assert names[0].value == "x"

    def test_comment_at_start(self):
        """Test comment at the start of code."""
        code = "-- comment\nx = 1"
        lexer = Lexer(code, language='english')
        tokens = lexer.tokenize()
        names = [t for t in tokens if t.type == TokenType.TK_NAME]
        assert len(names) == 1
        assert names[0].value == "x"

    def test_multiple_comments(self):
        """Test multiple comments."""
        code = """
-- comment 1
x = 1 -- comment 2
-- comment 3
y = 2
"""
        lexer = Lexer(code, language='english')
        tokens = lexer.tokenize()
        names = [t for t in tokens if t.type == TokenType.TK_NAME]
        assert len(names) == 2
        assert names[0].value == "x"
        assert names[1].value == "y"

    def test_empty_comment(self):
        """Test empty comment."""
        code = "x = 1 --\ny = 2"
        lexer = Lexer(code, language='english')
        tokens = lexer.tokenize()
        names = [t for t in tokens if t.type == TokenType.TK_NAME]
        assert len(names) == 2


class TestLineNumberTracking:
    """Test line number tracking in tokens."""

    def test_single_line_tokens(self):
        """Test that single-line tokens have correct line numbers."""
        code = "x = 1"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        for token in tokens:
            assert token.line == 1

    def test_multi_line_tokens(self):
        """Test line number tracking across multiple lines."""
        code = """x = 1
y = 2
z = 3"""
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        
        # Find tokens on each line
        line1_tokens = [t for t in tokens if t.line == 1]
        line2_tokens = [t for t in tokens if t.line == 2]
        line3_tokens = [t for t in tokens if t.line == 3]
        
        assert len(line1_tokens) > 0
        assert len(line2_tokens) > 0
        assert len(line3_tokens) > 0

    def test_line_numbers_after_comments(self):
        """Test line numbers are correct after comments."""
        code = """x = 1
-- comment
y = 2"""
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        
        y_token = next(t for t in tokens if t.type == TokenType.TK_NAME and t.value == "y")
        assert y_token.line == 3

    def test_line_numbers_in_long_strings(self):
        """Test line numbers with long strings spanning multiple lines."""
        code = '''x = [[line 1
line 2
line 3]]
y = 1'''
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        
        y_token = next(t for t in tokens if t.type == TokenType.TK_NAME and t.value == "y")
        assert y_token.line == 4


class TestShebangHandling:
    """Test shebang line handling."""

    def test_shebang_ignored(self):
        """Test that shebang line is ignored."""
        code = """#!/usr/bin/env lua
x = 1"""
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        
        names = [t for t in tokens if t.type == TokenType.TK_NAME]
        assert len(names) == 1
        assert names[0].value == "x"

    def test_no_shebang(self):
        """Test normal code without shebang."""
        code = "x = 1"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        assert len([t for t in tokens if t.type == TokenType.TK_NAME]) == 1


class TestWhitespaceHandling:
    """Test whitespace handling."""

    def test_spaces(self):
        """Test that spaces are ignored."""
        code1 = "x=1"
        code2 = "x = 1"
        code3 = "x  =  1"
        
        tokens1 = Lexer(code1).tokenize()
        tokens2 = Lexer(code2).tokenize()
        tokens3 = Lexer(code3).tokenize()
        
        assert len(tokens1) == len(tokens2) == len(tokens3)

    def test_tabs(self):
        """Test that tabs are ignored."""
        code = "x\t=\t1"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        assert len([t for t in tokens if t.type == TokenType.TK_NAME]) == 1

    def test_mixed_whitespace(self):
        """Test mixed whitespace."""
        code = "x \t = \t 1"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        assert len([t for t in tokens if t.type == TokenType.TK_NAME]) == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
