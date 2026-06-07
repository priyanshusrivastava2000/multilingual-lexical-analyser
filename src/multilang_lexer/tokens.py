"""
Token types, constants, and Token dataclass for the multilingual lexer.

Architecture:
- KEYWORD_TO_TOKEN is the canonical source mapping uppercase keyword names
  (e.g., "IF", "FUNCTION") to their TokenType values
- TOKEN_STRINGS is programmatically generated from KEYWORD_TO_TOKEN for
  error messages and debugging (converts to lowercase English)
- Language-specific reserved words are built dynamically in LexerState
  using KEYWORD_TO_TOKEN and translation JSON files
"""

from enum import IntEnum
from dataclasses import dataclass
from typing import Optional, Union


# Token types - values 0-255 are reserved for single ASCII characters
class TokenType(IntEnum):
    # First reserved token starts at 257 (above ASCII range)
    FIRST_RESERVED = 257

    # Reserved words (ORDER matters - matches token2string array)
    TK_AND = 257
    TK_BREAK = 258
    TK_DO = 259
    TK_ELSE = 260
    TK_ELSEIF = 261
    TK_END = 262
    TK_FOR = 263
    TK_FUNCTION = 264
    TK_IF = 265
    TK_IN = 266
    TK_LOCAL = 267
    TK_NIL = 268
    TK_NOT = 269
    TK_OR = 270
    TK_REPEAT = 271
    TK_RETURN = 272
    TK_THEN = 273
    TK_UNTIL = 274
    TK_WHILE = 275

    # Other tokens
    TK_CONCAT = 276    # ..
    TK_DOTS = 277      # ...
    TK_EQ = 278        # ==
    TK_GE = 279        # >=
    TK_LE = 280        # <=
    TK_NE = 281        # ~=
    TK_NUMBER = 282
    TK_STRING = 283
    TK_NAME = 284      # identifier
    TK_EOS = 285       # end of source


# Mapping from canonical keyword names to their TokenTypes
# This is the authoritative source for keyword-to-token mappings
KEYWORD_TO_TOKEN = {
    "AND": TokenType.TK_AND,
    "BREAK": TokenType.TK_BREAK,
    "DO": TokenType.TK_DO,
    "ELSE": TokenType.TK_ELSE,
    "ELSEIF": TokenType.TK_ELSEIF,
    "END": TokenType.TK_END,
    "FOR": TokenType.TK_FOR,
    "FUNCTION": TokenType.TK_FUNCTION,
    "IF": TokenType.TK_IF,
    "IN": TokenType.TK_IN,
    "LOCAL": TokenType.TK_LOCAL,
    "NIL": TokenType.TK_NIL,
    "NOT": TokenType.TK_NOT,
    "OR": TokenType.TK_OR,
    "REPEAT": TokenType.TK_REPEAT,
    "RETURN": TokenType.TK_RETURN,
    "THEN": TokenType.TK_THEN,
    "UNTIL": TokenType.TK_UNTIL,
    "WHILE": TokenType.TK_WHILE,
}

# Operator and special tokens that aren't keywords - explicit string mappings
_OPERATOR_STRINGS = {
    TokenType.TK_CONCAT: "..",
    TokenType.TK_DOTS: "...",
    TokenType.TK_EQ: "==",
    TokenType.TK_GE: ">=",
    TokenType.TK_LE: "<=",
    TokenType.TK_NE: "~=",
    TokenType.TK_NUMBER: "<number>",
    TokenType.TK_STRING: "<string>",
    TokenType.TK_NAME: "<name>",
    TokenType.TK_EOS: "<eof>",
}

# Token to string mapping for error messages and debugging
# Programmatically generated from KEYWORD_TO_TOKEN (converted to lowercase) + operators
TOKEN_STRINGS = {
    **{token_type: keyword.lower() for keyword, token_type in KEYWORD_TO_TOKEN.items()},
    **_OPERATOR_STRINGS
}


@dataclass
class Token:
    """Represents a lexical token."""
    type: Union[int, TokenType]  # int for single chars, TokenType for others
    value: Optional[Union[str, float]] = None  # semantic value (string or number)
    line: int = 1

    def __repr__(self):
        if isinstance(self.type, int) and self.type < 256:
            type_str = repr(chr(self.type))
        else:
            type_str = TOKEN_STRINGS.get(self.type, str(self.type))
        if self.value is not None:
            return f"Token({type_str}, {self.value!r}, line={self.line})"
        return f"Token({type_str}, line={self.line})"
