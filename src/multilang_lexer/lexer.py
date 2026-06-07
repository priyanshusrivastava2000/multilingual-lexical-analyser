"""
High-level lexer interface (facade pattern).
Delegates to LexerState, Tokenizer, and Detokenizer components.
Maintains backward compatibility with the original API.
"""

from typing import Union
from .tokens import Token, TokenType
from .lexer_state import LexerState
from .tokenizer import Tokenizer
from .detokenizer import Detokenizer


class Lexer:
    """
    Multilingual lexical analyzer that tokenizes source code.
    Supports multiple languages through JSON translation files.

    This class acts as a facade, delegating to:
    - LexerState: manages position, buffer, and language configuration
    - Tokenizer: performs tokenization logic
    - Detokenizer: converts tokens back to source code
    """

    def __init__(self, source: str, source_name: str = "<input>", language: str = 'english'):
        """
        Initialize the lexer.

        Args:
            source: Source code to tokenize
            source_name: Name of source (for error messages)
            language: Language for keyword translations ('english', 'spanish', 'mandarin')
        """
        self._state = LexerState(source, source_name, language)

    def lex(self) -> Token:
        """
        Get the next token from the source.

        Returns:
            The next token

        Raises:
            LexerError: If invalid syntax is encountered
        """
        return Tokenizer.lex_next_token(self._state)

    def tokenize(self) -> list[Token]:
        """
        Tokenize the entire source and return all tokens as a list.

        Returns:
            List of tokens including the final TK_EOS token

        Raises:
            LexerError: If invalid syntax is encountered
        """
        return Tokenizer.tokenize_all(self._state)

    def translate(self, tokens: list[Token], target_language: str) -> str:
        """
        Translate a token stream to source code in the target language.
        Enables bidirectional translation between languages.

        Args:
            tokens: List of tokens to translate
            target_language: Target language for keywords ('english', 'spanish', 'mandarin')

        Returns:
            Source code string with keywords in the target language
        """
        return Detokenizer.detokenize(tokens, target_language)

    def error(self, message: str, token: Union[int, TokenType, str] = ""):
        """
        Raise a lexer error.

        Args:
            message: Error message
            token: Token that caused the error

        Raises:
            LexerError: Always raised with formatted message
        """
        self._state.error(message, token)
