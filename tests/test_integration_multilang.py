"""
Integration tests for multi-language support.
Tests consistency across languages and language file loading.
"""

import pytest
from multilang_lexer import Lexer, Token, TokenType


class TestMultiLanguageConsistency:
    """Test that all three languages produce equivalent token streams."""

    def test_simple_function_all_languages(self):
        """Test simple function in all three languages."""
        english_code = "function test() end"
        spanish_code = "función test() fin"
        mandarin_code = "函数 test() 结束"
        
        eng_tokens = Lexer(english_code, language='english').tokenize()
        spa_tokens = Lexer(spanish_code, language='spanish').tokenize()
        man_tokens = Lexer(mandarin_code, language='mandarin').tokenize()
        
        # All should have same token types
        assert len(eng_tokens) == len(spa_tokens) == len(man_tokens)
        for e, s, m in zip(eng_tokens, spa_tokens, man_tokens):
            assert e.type == s.type == m.type

    def test_control_flow_all_languages(self):
        """Test control flow in all three languages."""
        english_code = "if x then return true else return false end"
        spanish_code = "si x entonces devolver true sino devolver false fin"
        mandarin_code = "如果 x 那么 返回 true 否则 返回 false 结束"
        
        eng_tokens = Lexer(english_code, language='english').tokenize()
        spa_tokens = Lexer(spanish_code, language='spanish').tokenize()
        man_tokens = Lexer(mandarin_code, language='mandarin').tokenize()
        
        for e, s, m in zip(eng_tokens, spa_tokens, man_tokens):
            assert e.type == s.type == m.type

    def test_loops_all_languages(self):
        """Test loop constructs in all three languages."""
        english_code = "while x do x = x - 1 end"
        spanish_code = "mientras x hacer x = x - 1 fin"
        mandarin_code = "当 x 执行 x = x - 1 结束"
        
        eng_tokens = Lexer(english_code, language='english').tokenize()
        spa_tokens = Lexer(spanish_code, language='spanish').tokenize()
        man_tokens = Lexer(mandarin_code, language='mandarin').tokenize()
        
        for e, s, m in zip(eng_tokens, spa_tokens, man_tokens):
            assert e.type == s.type == m.type


class TestLanguageLoading:
    """Test language file loading."""

    def test_english_language_loads(self):
        """Test English language file loads correctly."""
        lexer = Lexer("if x then end", language='english')
        tokens = lexer.tokenize()
        assert len(tokens) > 0

    def test_spanish_language_loads(self):
        """Test Spanish language file loads correctly."""
        lexer = Lexer("si x entonces fin", language='spanish')
        tokens = lexer.tokenize()
        assert len(tokens) > 0

    def test_mandarin_language_loads(self):
        """Test Mandarin language file loads correctly."""
        lexer = Lexer("如果 x 那么 结束", language='mandarin')
        tokens = lexer.tokenize()
        assert len(tokens) > 0

    def test_invalid_language_raises_error(self):
        """Test that invalid language raises error."""
        with pytest.raises(FileNotFoundError):
            Lexer("test", language='invalid_language')


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
