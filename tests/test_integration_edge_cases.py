"""
Integration tests for edge cases and performance.
Tests boundary conditions, extreme inputs, and performance scenarios.
"""

import pytest
from multilang_lexer import Lexer, Token, TokenType


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_empty_source(self):
        """Test empty source code."""
        lexer = Lexer("")
        tokens = lexer.tokenize()
        assert len(tokens) == 1
        assert tokens[0].type == TokenType.TK_EOS

    def test_only_whitespace(self):
        """Test source with only whitespace."""
        lexer = Lexer("   \t\n\r\n   ")
        tokens = lexer.tokenize()
        assert len(tokens) == 1
        assert tokens[0].type == TokenType.TK_EOS

    def test_only_comments(self):
        """Test source with only comments."""
        code = """-- comment 1
-- comment 2
-- comment 3"""
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        assert len(tokens) == 1
        assert tokens[0].type == TokenType.TK_EOS

    def test_single_character_tokens(self):
        """Test all single character tokens."""
        code = "+ - * / ^ % # ( ) { } [ ] ; : , . < > = ~"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        # All should be single char tokens (< 256)
        char_tokens = [t for t in tokens if t.type < 256 and t.type != TokenType.TK_EOS]
        assert len(char_tokens) > 15

    def test_consecutive_operators(self):
        """Test consecutive operators without spaces."""
        code = "x==y<=z>=a~=b..c...d"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        
        assert any(t.type == TokenType.TK_EQ for t in tokens)
        assert any(t.type == TokenType.TK_LE for t in tokens)
        assert any(t.type == TokenType.TK_GE for t in tokens)
        assert any(t.type == TokenType.TK_NE for t in tokens)
        assert any(t.type == TokenType.TK_CONCAT for t in tokens)
        assert any(t.type == TokenType.TK_DOTS for t in tokens)

    def test_number_followed_by_identifier(self):
        """Test number immediately followed by identifier (should be separate tokens)."""
        code = "123abc"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        
        # Should tokenize as number then name
        assert tokens[0].type == TokenType.TK_NUMBER
        assert tokens[1].type == TokenType.TK_NAME

    def test_very_long_identifier(self):
        """Test very long identifier names."""
        long_name = "a" * 1000
        lexer = Lexer(long_name)
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.TK_NAME
        assert len(tokens[0].value) == 1000

    def test_very_long_string(self):
        """Test very long string literals."""
        long_string = '"' + "x" * 10000 + '"'
        lexer = Lexer(long_string)
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.TK_STRING
        assert len(tokens[0].value) == 10000

    def test_deeply_nested_long_strings(self):
        """Test deeply nested long string literals."""
        code = "[[level1 [[level2 [[level3]] level2]] level1]]"
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        assert tokens[0].type == TokenType.TK_STRING
        assert "level1" in tokens[0].value
        assert "level2" in tokens[0].value
        assert "level3" in tokens[0].value


class TestPerformance:
    """Test performance with large inputs."""

    def test_large_file_tokenization(self):
        """Test tokenizing a large file."""
        # Create a large program with 100 functions
        functions = []
        for i in range(100):
            functions.append(f"""
function func{i}(x, y)
    if x > 0 then
        return x + y
    else
        return x - y
    end
end
""")
        
        code = "\n".join(functions)
        lexer = Lexer(code, language='english')
        tokens = lexer.tokenize()
        
        # Should have successfully tokenized
        assert len(tokens) > 1000
        functions_count = sum(1 for t in tokens if t.type == TokenType.TK_FUNCTION)
        assert functions_count == 100

    def test_deeply_nested_structures(self):
        """Test deeply nested if-else structures."""
        depth = 50
        code = ""
        for i in range(depth):
            code += f"if x{i} then "
        code += "return true "
        for i in range(depth):
            code += "end "
        
        lexer = Lexer(code, language='english')
        tokens = lexer.tokenize()
        
        ifs = sum(1 for t in tokens if t.type == TokenType.TK_IF)
        ends = sum(1 for t in tokens if t.type == TokenType.TK_END)
        
        assert ifs == depth
        assert ends == depth


class TestTokenRepresentation:
    """Test Token class representation and equality."""

    def test_token_repr_keyword(self):
        """Test Token repr for keywords."""
        token = Token(TokenType.TK_IF, line=1)
        repr_str = repr(token)
        assert "if" in repr_str
        assert "line=1" in repr_str

    def test_token_repr_with_value(self):
        """Test Token repr with value."""
        token = Token(TokenType.TK_NUMBER, 42.0, line=5)
        repr_str = repr(token)
        assert "42" in repr_str
        assert "line=5" in repr_str

    def test_token_repr_char(self):
        """Test Token repr for character tokens."""
        token = Token(ord('+'), line=1)
        repr_str = repr(token)
        assert "+" in repr_str


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
