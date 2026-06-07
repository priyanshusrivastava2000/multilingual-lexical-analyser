"""
Multilingual Lexical Analyzer

A lexer that supports multiple languages through JSON translation files.
Based on the Lua 4.0 lexer, extended to support arbitrary languages.
"""

from .lexer import Lexer
from .tokens import Token, TokenType
from .exceptions import LexerError

__version__ = "0.1.0"

__all__ = [
    "Lexer",
    "Token",
    "TokenType",
    "LexerError",
]
