"""
Integration tests for complete tokenization/detokenization workflows.
Tests end-to-end functionality and real-world programs.
"""

import pytest
from multilang_lexer import Lexer, Token, TokenType, LexerError
from multilang_lexer.detokenizer import Detokenizer


class TestCompleteWorkflows:
    """Test complete tokenization and detokenization workflows."""

    def test_tokenize_and_detokenize_roundtrip(self):
        """Test that tokenize->detokenize produces equivalent code."""
        code = '''
function factorial(n)
    if n <= 1 then
        return 1
    else
        return n * factorial(n - 1)
    end
end
'''
        lexer = Lexer(code, language='english')
        tokens = lexer.tokenize()
        result = Detokenizer.detokenize(tokens, target_language='english')
        
        # Re-tokenize the result and compare token types
        lexer2 = Lexer(result, language='english')
        tokens2 = lexer2.tokenize()
        
        assert len(tokens) == len(tokens2)
        for t1, t2 in zip(tokens, tokens2):
            assert t1.type == t2.type

    def test_cross_language_translation_english_to_spanish(self):
        """Test translating English code to Spanish."""
        english_code = "if x > 0 then return true else return false end"
        
        lexer = Lexer(english_code, language='english')
        tokens = lexer.tokenize()
        spanish_code = Detokenizer.detokenize(tokens, target_language='spanish')
        
        # Verify Spanish keywords are present
        assert 'si' in spanish_code  # if
        assert 'entonces' in spanish_code  # then
        assert 'sino' in spanish_code  # else
        assert 'devolver' in spanish_code  # return
        assert 'fin' in spanish_code  # end

    def test_cross_language_translation_english_to_mandarin(self):
        """Test translating English code to Mandarin."""
        english_code = "function test(n) while n > 0 do n = n - 1 end end"
        
        lexer = Lexer(english_code, language='english')
        tokens = lexer.tokenize()
        mandarin_code = Detokenizer.detokenize(tokens, target_language='mandarin')
        
        # Verify Mandarin keywords are present
        assert '函数' in mandarin_code  # function
        assert '当' in mandarin_code  # while
        assert '执行' in mandarin_code  # do
        assert '结束' in mandarin_code  # end

    def test_spanish_to_english_translation(self):
        """Test translating Spanish code to English."""
        spanish_code = "si x > 0 entonces devolver verdadero sino devolver falso fin"
        
        lexer = Lexer(spanish_code, language='spanish')
        tokens = lexer.tokenize()
        english_code = Detokenizer.detokenize(tokens, target_language='english')
        
        assert 'if' in english_code
        assert 'then' in english_code
        assert 'else' in english_code
        assert 'return' in english_code
        assert 'end' in english_code

    def test_mandarin_to_english_translation(self):
        """Test translating Mandarin code to English."""
        mandarin_code = "如果 x > 0 那么 返回 1 结束"
        
        lexer = Lexer(mandarin_code, language='mandarin')
        tokens = lexer.tokenize()
        english_code = Detokenizer.detokenize(tokens, target_language='english')
        
        assert 'if' in english_code
        assert 'then' in english_code
        assert 'return' in english_code
        assert 'end' in english_code


class TestCompletePrograms:
    """Test complete, realistic programs."""

    def test_fibonacci_function(self):
        """Test tokenizing a complete Fibonacci function."""
        code = '''
function fibonacci(n)
    if n <= 1 then
        return n
    else
        return fibonacci(n - 1) + fibonacci(n - 2)
    end
end
'''
        lexer = Lexer(code, language='english')
        tokens = lexer.tokenize()
        
        # Verify we got all expected tokens
        assert any(t.type == TokenType.TK_FUNCTION for t in tokens)
        assert any(t.type == TokenType.TK_IF for t in tokens)
        assert any(t.type == TokenType.TK_RETURN for t in tokens)
        assert any(t.type == TokenType.TK_END for t in tokens)
        
        # Translate to Spanish and verify
        spanish = Detokenizer.detokenize(tokens, target_language='spanish')
        assert 'función' in spanish
        assert 'si' in spanish
        assert 'devolver' in spanish

    def test_bubble_sort(self):
        """Test tokenizing a bubble sort implementation."""
        code = '''
function bubbleSort(arr)
    local n = 0
    for i = 1, n do
        for j = 1, n - i do
            if arr > arr then
                local temp = arr
                arr = arr
                arr = temp
            end
        end
    end
    return arr
end
'''
        lexer = Lexer(code, language='english')
        tokens = lexer.tokenize()
        
        # Count keywords
        functions = sum(1 for t in tokens if t.type == TokenType.TK_FUNCTION)
        locals = sum(1 for t in tokens if t.type == TokenType.TK_LOCAL)
        fors = sum(1 for t in tokens if t.type == TokenType.TK_FOR)
        ifs = sum(1 for t in tokens if t.type == TokenType.TK_IF)
        
        assert functions == 1
        assert locals == 2
        assert fors == 2
        assert ifs == 1

    def test_class_like_structure(self):
        """Test tokenizing a class-like structure."""
        code = '''
local Object = {}

function Object:new()
    local obj = {}
    return obj
end

function Object:method(x, y)
    if x and y then
        return x + y
    else
        return nil
    end
end
'''
        lexer = Lexer(code, language='english')
        tokens = lexer.tokenize()
        
        functions = sum(1 for t in tokens if t.type == TokenType.TK_FUNCTION)
        locals = sum(1 for t in tokens if t.type == TokenType.TK_LOCAL)
        returns = sum(1 for t in tokens if t.type == TokenType.TK_RETURN)
        
        assert functions == 2
        assert locals == 2
        assert returns == 3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
