"""
Exception classes for the multilingual lexer.
"""


class LexerError(Exception):
    """Exception raised for lexical analysis errors."""
    def __init__(self, message: str, line: int, token: str = ""):
        self.message = message
        self.line = line
        self.token = token
        super().__init__(f"{message} at line {line}" + (f" near '{token}'" if token else ""))
