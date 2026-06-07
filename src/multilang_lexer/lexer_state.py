"""
Lexer state management for the multilingual lexical analyzer.
Handles position tracking, character buffering, and language configuration.
"""

from typing import Union
from .tokens import TokenType, TOKEN_STRINGS, KEYWORD_TO_TOKEN
from .exceptions import LexerError
from .languages import load_language


class LexerState:
    """
    Manages the state for lexical analysis.

    This class maintains:
    - Source code and current position
    - Character buffer for building tokens
    - Line number tracking
    - Language-specific keyword mappings
    """

    def __init__(self, source: str, source_name: str = "<input>", language: str = 'english'):
        """
        Initialize lexer state.

        Args:
            source: Source code to tokenize
            source_name: Name of source (for error messages)
            language: Language for keyword translations
        """
        self.source = source
        self.source_name = source_name
        self.pos = 0                    # current position in source
        self.current = ''               # current character
        self.linenumber = 1
        self.lastline = 1
        self.buffer = []                # buffer for building tokens

        self.language = language
        self.translations = load_language(language)
        self.reserved_words = self._build_reserved_words()

        # Read first character
        self._next()

        # Skip shebang line (starts with #)
        if self.current == '#':
            while self.current and self.current != '\n':
                self._next()

    def _build_reserved_words(self) -> dict:
        """
        Build a mapping from language-specific keywords to TokenTypes.
        Uses the translations loaded for the current language.

        Returns:
            Dictionary mapping translated keywords to TokenType values
        """
        reserved = {}
        for keyword_name, token_type in KEYWORD_TO_TOKEN.items():
            translated_keyword = self.translations[keyword_name]
            reserved[translated_keyword] = token_type
        return reserved

    def _next(self):
        """Advance to next character (equivalent to next() macro in C)."""
        if self.pos < len(self.source):
            self.current = self.source[self.pos]
            self.pos += 1
        else:
            self.current = ''  # Empty string signals EOZ (end of input)

    def _save(self, c: str):
        """Save character to buffer."""
        self.buffer.append(c)

    def _save_and_next(self):
        """Save current character and advance."""
        self._save(self.current)
        self._next()

    def _clear_buffer(self):
        """Clear the token buffer."""
        self.buffer = []

    def _get_buffer(self) -> str:
        """Get buffer contents as string."""
        return ''.join(self.buffer)

    def _inclinenumber(self):
        """Increment line number (after seeing newline)."""
        self._next()  # skip the newline
        self.linenumber += 1

    def error(self, message: str, token: Union[int, TokenType, str] = ""):
        """
        Raise a lexer error.

        Args:
            message: Error message
            token: Token that caused the error (int, TokenType, or string)

        Raises:
            LexerError: Always raised with formatted message
        """
        if isinstance(token, int):
            if token < 256:
                token_str = chr(token)
            else:
                token_str = TOKEN_STRINGS.get(token, str(token))
        elif isinstance(token, TokenType):
            token_str = TOKEN_STRINGS.get(token, str(token))
        else:
            token_str = str(token)
        raise LexerError(message, self.linenumber, token_str)