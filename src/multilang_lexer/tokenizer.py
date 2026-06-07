"""
Tokenization logic for the multilingual lexical analyzer.
All methods are static and operate on LexerState instances.
"""

from .tokens import Token, TokenType
from .lexer_state import LexerState


class Tokenizer:
    """
    Stateless tokenization methods that operate on LexerState.
    All methods are static to emphasize they don't maintain their own state.
    """

    @staticmethod
    def read_name(state: LexerState) -> str:
        """
        Read an identifier or keyword, supporting Unicode characters for non-English languages.

        Args:
            state: Current lexer state

        Returns:
            The identifier/keyword string
        """
        state._clear_buffer()
        while (state.current.isalnum() or
               state.current == '_' or
               (state.current and ord(state.current) > 127)):  # Support Unicode characters
            state._save_and_next()
        return state._get_buffer()

    @staticmethod
    def read_number(state: LexerState, starts_with_dot: bool = False) -> int | float:
        """
        Read a numeric literal.

        Args:
            state: Current lexer state
            starts_with_dot: Whether the number starts with a decimal point

        Returns:
            The numeric value as an int or float

        Raises:
            LexerError: If the number is malformed
        """
        state._clear_buffer()

        if starts_with_dot:
            state._save('.')

        # Integer part
        while state.current.isdigit():
            state._save_and_next()

        # Decimal part
        if state.current == '.':
            state._save_and_next()
            # Check for '..' (concatenation) - this is an error in number context
            if state.current == '.':
                state._save_and_next()
                state.error("ambiguous syntax (decimal point x string concatenation)",
                          TokenType.TK_NUMBER)

        # Fractional digits
        while state.current.isdigit():
            state._save_and_next()

        # Exponent part
        if state.current in ('e', 'E'):
            state._save_and_next()
            if state.current in ('+', '-'):
                state._save_and_next()
            while state.current.isdigit():
                state._save_and_next()

        num_str = state._get_buffer()
        try:
            # Check if this is actually an integer (no decimal point, no exponent)
            if '.' not in num_str and 'e' not in num_str.lower():
                return int(num_str)
            else:
                return float(num_str)
        except ValueError:
            state.error("malformed number", TokenType.TK_NUMBER)

    @staticmethod
    def read_long_string(state: LexerState) -> str:
        """
        Read a long string literal [[...]].

        Args:
            state: Current lexer state

        Returns:
            The string content (without surrounding [[ and ]])

        Raises:
            LexerError: If the string is not properly terminated
        """
        state._clear_buffer()
        nesting = 0

        state._save('[')           # save first '['
        state._save_and_next()     # save second '[' and advance

        while True:
            if not state.current:  # EOZ
                state.error("unfinished long string", TokenType.TK_STRING)

            elif state.current == '[':
                state._save_and_next()
                if state.current == '[':
                    nesting += 1
                    state._save_and_next()

            elif state.current == ']':
                state._save_and_next()
                if state.current == ']':
                    if nesting == 0:
                        state._save_and_next()  # skip second ']'
                        break
                    nesting -= 1
                    state._save_and_next()

            elif state.current == '\n':
                state._save('\n')
                state._inclinenumber()

            else:
                state._save_and_next()

        # Return content without the surrounding [[ and ]]
        content = state._get_buffer()
        return content[2:-2]

    @staticmethod
    def read_string(state: LexerState, delimiter: str) -> str:
        """
        Read a string literal (single or double quoted).

        Args:
            state: Current lexer state
            delimiter: Quote character (' or ")

        Returns:
            The string content (without surrounding quotes)

        Raises:
            LexerError: If the string is not properly terminated or has invalid escapes
        """
        state._clear_buffer()
        state._save_and_next()  # save and skip opening delimiter

        while state.current != delimiter:
            if not state.current or state.current == '\n':
                state.error("unfinished string", TokenType.TK_STRING)

            elif state.current == '\\':
                state._next()  # skip backslash

                # Escape sequences
                escape_map = {
                    'a': '\a', 'b': '\b', 'f': '\f', 'n': '\n',
                    'r': '\r', 't': '\t', 'v': '\v',
                    '\\': '\\', '"': '"', "'": "'", '?': '?'
                }

                if state.current in escape_map:
                    state._save(escape_map[state.current])
                    state._next()

                elif state.current == '\n':
                    state._save('\n')
                    state._inclinenumber()

                elif state.current.isdigit():
                    # Numeric escape \ddd (up to 3 digits)
                    value = 0
                    count = 0
                    while count < 3 and state.current.isdigit():
                        value = value * 10 + int(state.current)
                        state._next()
                        count += 1
                    if value > 255:
                        state.error("escape sequence too large", TokenType.TK_STRING)
                    state._save(chr(value))

                else:
                    # Unknown escape - just save the character
                    state._save_and_next()

            else:
                state._save_and_next()

        state._save_and_next()  # save and skip closing delimiter

        # Return content without the surrounding quotes
        content = state._get_buffer()
        return content[1:-1]

    @staticmethod
    def lex_next_token(state: LexerState) -> Token:
        """
        Main lexer function - returns the next token.
        Equivalent to luaX_lex in the C code.

        Args:
            state: Current lexer state

        Returns:
            The next token from the input

        Raises:
            LexerError: If invalid syntax is encountered
        """
        while True:
            # Whitespace (space, tab, carriage return)
            if state.current in (' ', '\t', '\r'):
                state._next()
                continue

            # Newline
            if state.current == '\n':
                state._inclinenumber()
                continue

            # End of input
            if not state.current:
                return Token(TokenType.TK_EOS, line=state.linenumber)

            # Dollar sign (pragmas no longer supported)
            if state.current == '$':
                state.error("unexpected `$' (pragmas are no longer supported)", '$')

            # Minus or comment
            if state.current == '-':
                state._next()
                if state.current != '-':
                    return Token(ord('-'), line=state.linenumber)
                # Comment - skip until end of line
                while state.current and state.current != '\n':
                    state._next()
                continue

            # Long string or left bracket
            if state.current == '[':
                state._next()
                if state.current != '[':
                    return Token(ord('['), line=state.linenumber)
                value = Tokenizer.read_long_string(state)
                return Token(TokenType.TK_STRING, value, state.linenumber)

            # Equality operators
            if state.current == '=':
                state._next()
                if state.current != '=':
                    return Token(ord('='), line=state.linenumber)
                state._next()
                return Token(TokenType.TK_EQ, line=state.linenumber)

            if state.current == '<':
                state._next()
                if state.current != '=':
                    return Token(ord('<'), line=state.linenumber)
                state._next()
                return Token(TokenType.TK_LE, line=state.linenumber)

            if state.current == '>':
                state._next()
                if state.current != '=':
                    return Token(ord('>'), line=state.linenumber)
                state._next()
                return Token(TokenType.TK_GE, line=state.linenumber)

            if state.current == '~':
                state._next()
                if state.current != '=':
                    return Token(ord('~'), line=state.linenumber)
                state._next()
                return Token(TokenType.TK_NE, line=state.linenumber)

            # String literals
            if state.current in ('"', "'"):
                delimiter = state.current
                value = Tokenizer.read_string(state, delimiter)
                return Token(TokenType.TK_STRING, value, state.linenumber)

            # Dot, concat, dots, or number starting with dot
            if state.current == '.':
                state._next()
                if state.current == '.':
                    state._next()
                    if state.current == '.':
                        state._next()
                        return Token(TokenType.TK_DOTS, line=state.linenumber)
                    return Token(TokenType.TK_CONCAT, line=state.linenumber)
                if not state.current.isdigit():
                    return Token(ord('.'), line=state.linenumber)
                # Number starting with decimal point
                value = Tokenizer.read_number(state, starts_with_dot=True)
                return Token(TokenType.TK_NUMBER, value, state.linenumber)

            # Numbers
            if state.current.isdigit():
                value = Tokenizer.read_number(state)
                return Token(TokenType.TK_NUMBER, value, state.linenumber)

            # Identifiers and reserved words (including Unicode characters for non-English)
            if state.current.isalpha() or state.current == '_' or (state.current and ord(state.current) > 127):
                name = Tokenizer.read_name(state)
                # Check if it's a reserved word in the current language
                if name in state.reserved_words:
                    return Token(state.reserved_words[name], line=state.linenumber)
                return Token(TokenType.TK_NAME, name, state.linenumber)

            # Control characters are invalid
            if state.current.isprintable() is False and state.current not in ('\n', '\t', '\r'):
                state.error(f"invalid control char", f"0x{ord(state.current):02X}")

            # Single character token (operators, punctuation)
            c = state.current
            state._next()
            return Token(ord(c), line=state.linenumber)

    @staticmethod
    def tokenize_all(state: LexerState) -> list[Token]:
        """
        Tokenize the entire source and return all tokens as a list.
        Convenience method that calls lex_next_token() repeatedly until TK_EOS.

        Args:
            state: Current lexer state

        Returns:
            List of tokens including the final TK_EOS token
        """
        tokens = []
        while True:
            token = Tokenizer.lex_next_token(state)
            tokens.append(token)
            if token.type == TokenType.TK_EOS:
                break
        return tokens