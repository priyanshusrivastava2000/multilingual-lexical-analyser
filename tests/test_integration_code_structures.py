"""
Integration tests for complex code structures.
Tests nested control flow, loops, and complex expressions.
"""

import pytest
from multilang_lexer import Lexer, TokenType


class TestComplexCodeStructures:
    """Test complex, real-world code structures."""

    def test_nested_control_flow(self):
        """Test deeply nested control flow structures."""
        code = '''
function complex(x, y)
    if x > 0 then
        if y > 0 then
            return x + y
        elseif y < 0 then
            return x - y
        else
            return x
        end
    else
        if y > 0 then
            return y
        else
            return 0
        end
    end
end
'''
        lexer = Lexer(code, language='english')
        tokens = lexer.tokenize()
        
        # Count different token types
        functions = sum(1 for t in tokens if t.type == TokenType.TK_FUNCTION)
        ifs = sum(1 for t in tokens if t.type == TokenType.TK_IF)
        elseifs = sum(1 for t in tokens if t.type == TokenType.TK_ELSEIF)
        elses = sum(1 for t in tokens if t.type == TokenType.TK_ELSE)
        ends = sum(1 for t in tokens if t.type == TokenType.TK_END)
        returns = sum(1 for t in tokens if t.type == TokenType.TK_RETURN)
        
        assert functions == 1
        assert ifs == 3
        assert elseifs == 1
        assert elses == 3
        assert ends == 4
        assert returns == 5

    def test_multiple_loops(self):
        """Test various loop structures."""
        code = '''
for i = 1, 10 do
    while x > 0 do
        x = x - 1
    end
end

repeat
    y = y + 1
until y >= 10
'''
        lexer = Lexer(code, language='english')
        tokens = lexer.tokenize()
        
        fors = sum(1 for t in tokens if t.type == TokenType.TK_FOR)
        whiles = sum(1 for t in tokens if t.type == TokenType.TK_WHILE)
        repeats = sum(1 for t in tokens if t.type == TokenType.TK_REPEAT)
        untils = sum(1 for t in tokens if t.type == TokenType.TK_UNTIL)
        dos = sum(1 for t in tokens if t.type == TokenType.TK_DO)
        
        assert fors == 1
        assert whiles == 1
        assert repeats == 1
        assert untils == 1
        assert dos == 2  # for...do and while...do

    def test_complex_expressions(self):
        """Test complex mathematical and logical expressions."""
        code = "result = (a + b) * (c - d) / e and x or y and not z"
        
        lexer = Lexer(code, language='english')
        tokens = lexer.tokenize()
        
        ands = sum(1 for t in tokens if t.type == TokenType.TK_AND)
        ors = sum(1 for t in tokens if t.type == TokenType.TK_OR)
        nots = sum(1 for t in tokens if t.type == TokenType.TK_NOT)
        
        assert ands == 2
        assert ors == 1
        assert nots == 1

    def test_multiple_function_definitions(self):
        """Test multiple function definitions."""
        code = '''
function add(a, b)
    return a + b
end

local function multiply(a, b)
    return a * b
end

function divide(a, b)
    if b ~= 0 then
        return a / b
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
        nils = sum(1 for t in tokens if t.type == TokenType.TK_NIL)
        
        assert functions == 3
        assert locals == 1
        assert returns == 4
        assert nils == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
