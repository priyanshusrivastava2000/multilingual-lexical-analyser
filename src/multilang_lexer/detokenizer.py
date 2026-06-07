"""
Detokenization logic for the multilingual lexical analyzer.
Converts token streams back to source code strings.
All methods are static and operate on token lists.
"""

from .tokens import Token, TokenType, KEYWORD_TO_TOKEN
from .languages import load_language


def _build_target_keywords(target_language: str) -> set[str]:
    """Build set of keywords in target language."""
    translations = load_language(target_language)
    return set(translations.values())


def _generate_safe_name(original: str, target_keywords: set, used_names: set) -> str:
    """Generate conflict-free identifier by adding underscores."""
    candidate = "_" + original
    while candidate in target_keywords or candidate in used_names:
        candidate = "_" + candidate
    return candidate


def _build_rename_mapping(tokens: list[Token], target_keywords: set) -> dict[str, str]:
    """Build mapping from conflicting identifiers to safe names."""
    # Collect all unique identifier names
    identifiers = set()
    for token in tokens:
        if token.type == TokenType.TK_NAME:
            identifiers.add(token.value)

    # Build rename mapping for conflicts
    rename_mapping = {}
    used_names = set(identifiers)

    for identifier in identifiers:
        if identifier in target_keywords:
            safe_name = _generate_safe_name(identifier, target_keywords, used_names)
            rename_mapping[identifier] = safe_name
            used_names.add(safe_name)

    return rename_mapping


class Detokenizer:
    """
    Stateless detokenization methods.
    All methods are static to emphasize they don't maintain their own state.
    """

    @staticmethod
    def format_token(token: Token, language: str = 'english', rename_mapping: dict[str, str] = None) -> str:
        """
        Format a single token as a string in the target language.

        Args:
            token: Token to format
            language: Target language for keywords
            rename_mapping: Optional mapping for renaming identifiers

        Returns:
            String representation of the token, or empty string for TK_EOS
        """
        if rename_mapping is None:
            rename_mapping = {}

        translations = load_language(language)

        # Keyword tokens - translate to target language
        if token.type in KEYWORD_TO_TOKEN.values():
            for keyword_name, token_type in KEYWORD_TO_TOKEN.items():
                if token_type == token.type:
                    return translations[keyword_name]

        # String literal
        if token.type == TokenType.TK_STRING:
            return f'"{token.value}"'

        # Number literal
        if token.type == TokenType.TK_NUMBER:
            return str(token.value)

        # Identifier - check for rename
        if token.type == TokenType.TK_NAME:
            original_name = token.value
            return rename_mapping.get(original_name, original_name)

        # Single character token
        if token.type < 256:
            return chr(token.type)

        # Multi-character operators
        if token.type == TokenType.TK_CONCAT:
            return '..'
        if token.type == TokenType.TK_DOTS:
            return '...'
        if token.type == TokenType.TK_EQ:
            return '=='
        if token.type == TokenType.TK_GE:
            return '>='
        if token.type == TokenType.TK_LE:
            return '<='
        if token.type == TokenType.TK_NE:
            return '~='

        # TK_EOS - return empty string
        return ''

    @staticmethod
    def detokenize(tokens: list[Token], target_language: str = 'english') -> str:
        """
        Convert a list of tokens back to source code in the target language.
        Automatically resolves identifier conflicts with target language keywords.

        Args:
            tokens: List of tokens to convert
            target_language: Language for keywords (default: 'english')

        Returns:
            Source code string with keywords in the target language and
            conflicting identifiers renamed to avoid keyword conflicts
        """
        # PHASE 1: Build rename mapping for conflict resolution
        target_keywords = _build_target_keywords(target_language)
        rename_mapping = _build_rename_mapping(tokens, target_keywords)

        # PHASE 2: Format tokens
        output = []
        current_line = 1
        indent_level = 0
        prev_token = None

        # Keywords that increase indent on the next line
        indent_after = {TokenType.TK_FUNCTION, TokenType.TK_THEN, TokenType.TK_DO, TokenType.TK_REPEAT}
        # Keywords that decrease indent before printing
        dedent_before = {TokenType.TK_END, TokenType.TK_UNTIL, TokenType.TK_ELSEIF}
        # Keywords that dedent then indent (else only - elseif relies on subsequent 'then')
        dedent_then_indent = {TokenType.TK_ELSE}

        # Tokens that should not have space before them
        no_space_before = {ord('('), ord('['), ord(')'), ord(']'), ord(','), ord(';')}
        # Tokens that should not have space after them
        no_space_after = {ord('('), ord('[')}

        for i, token in enumerate(tokens):
            formatted = Detokenizer.format_token(token, target_language, rename_mapping)
            if formatted:  # Skip empty strings (TK_EOS)
                # Handle newline and indentation
                if token.line > current_line:
                    # Check if we need to dedent before this token
                    if token.type in dedent_before:
                        indent_level = max(0, indent_level - 1)
                    elif token.type in dedent_then_indent:
                        indent_level = max(0, indent_level - 1)

                    # Add newline and indentation
                    output.append('\n' * (token.line - current_line))
                    output.append('    ' * indent_level)
                    current_line = token.line
                else:
                    # Same line - add space if needed
                    if output and prev_token is not None:
                        # Check if we should add space based on previous and current token
                        should_space = (prev_token.type not in no_space_after and
                                      token.type not in no_space_before)
                        if should_space:
                            output.append(' ')

                output.append(formatted)
                prev_token = token

                # Check if we need to indent after this token
                if token.type in indent_after:
                    indent_level += 1
                elif token.type in dedent_then_indent:
                    indent_level += 1

        return ''.join(output)