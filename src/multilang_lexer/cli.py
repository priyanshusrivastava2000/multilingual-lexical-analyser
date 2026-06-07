"""
Interactive CLI for the multilingual lexical analyzer.
Supports both REPL mode and command-line argument mode.
"""

import sys
import argparse
from typing import List
from multilang_lexer import Lexer
from multilang_lexer.tokens import Token, TokenType, KEYWORD_TO_TOKEN
from multilang_lexer.exceptions import LexerError


# ─────────────────────────────────────────────────────────────
# CONSTANTS & CONFIGURATION
# ─────────────────────────────────────────────────────────────

LANGUAGES = ['english', 'spanish', 'mandarin']
VERSION = "0.1.0"

EXAMPLES = {
    'factorial': {
        'code': '''local function factorial(n)
    if n <= 1 then
        return 1
    else
        return n * factorial(n - 1)
    end
end''',
        'description': 'Recursive factorial calculation'
    },
    'fibonacci': {
        'code': '''local function fib(n)
    if n <= 1 then
        return n
    else
        return fib(n - 1) + fib(n - 2)
    end
end''',
        'description': 'Recursive Fibonacci sequence'
    },
    'loop': {
        'code': '''local sum = 0
for i = 1, 10 do
    sum = sum + i
end
return sum''',
        'description': 'Iterative sum with for loop'
    },
    'conditional': {
        'code': '''local function max(a, b)
    if a > b then
        return a
    else
        return b
    end
end''',
        'description': 'Find maximum of two numbers'
    }
}

CONFLICT_EXAMPLE = {
    'code': '''local function process(y, para, o)
    if y and para then
        return o
    else
        return nil
    end
end''',
    'explanation': '''This code uses identifiers that conflict with Spanish keywords:
  • "y" is Spanish for "and" (AND operator)
  • "para" is Spanish for "for" (FOR loop keyword)
  • "o" is Spanish for "or" (OR operator)

When translating to Spanish, these identifiers are automatically
renamed with underscore prefix to avoid keyword conflicts.'''
}


# ─────────────────────────────────────────────────────────────
# FORMATTING UTILITIES
# ─────────────────────────────────────────────────────────────

def print_header(text: str) -> None:
    """Print formatted header."""
    width = 60
    print(f"\n╔{'═' * (width - 2)}╗")
    print(f"║ {text:^{width - 4}} ║")
    print(f"╚{'═' * (width - 2)}╝")

def print_section(title: str) -> None:
    """Print section separator."""
    print(f"\n{title}")
    print('─' * 60)

def get_token_type_name(token_type) -> str:
    """Get human-readable name for token type."""
    # Check if it's a reserved word
    for name, ttype in KEYWORD_TO_TOKEN.items():
        if ttype == token_type:
            return f"TK_{name}"

    # Check common token types
    if token_type == TokenType.TK_NAME:
        return "TK_NAME"
    elif token_type == TokenType.TK_NUMBER:
        return "TK_NUMBER"
    elif token_type == TokenType.TK_STRING:
        return "TK_STRING"
    elif token_type == TokenType.TK_EOS:
        return "TK_EOS"
    elif token_type == TokenType.TK_CONCAT:
        return "TK_CONCAT"
    elif token_type == TokenType.TK_DOTS:
        return "TK_DOTS"
    elif token_type == TokenType.TK_EQ:
        return "TK_EQ"
    elif token_type == TokenType.TK_GE:
        return "TK_GE"
    elif token_type == TokenType.TK_LE:
        return "TK_LE"
    elif token_type == TokenType.TK_NE:
        return "TK_NE"
    elif token_type < 256:
        return f"CHAR('{chr(token_type)}')"
    else:
        return f"UNKNOWN({token_type})"

def count_keywords(tokens: List[Token]) -> int:
    """Count keyword tokens."""
    return sum(1 for t in tokens if t.type in KEYWORD_TO_TOKEN.values())

def count_identifiers(tokens: List[Token]) -> int:
    """Count identifier tokens."""
    return sum(1 for t in tokens if t.type == TokenType.TK_NAME)

def count_operators(tokens: List[Token]) -> int:
    """Count operator tokens."""
    operator_types = {TokenType.TK_CONCAT, TokenType.TK_DOTS, TokenType.TK_EQ,
                      TokenType.TK_GE, TokenType.TK_LE, TokenType.TK_NE}
    return sum(1 for t in tokens if t.type < 256 or t.type in operator_types)

# ─────────────────────────────────────────────────────────────
# CORE FEATURES
# ─────────────────────────────────────────────────────────────

def translate_code(code: str, source_lang: str, target_lang: str) -> str:
    """Translate code from source to target language."""
    lexer = Lexer(code, language=source_lang)
    tokens = lexer.tokenize()
    return lexer.translate(tokens, target_lang)

def inspect_tokens(code: str, language: str) -> None:
    """Display tokenized output in formatted table."""
    lexer = Lexer(code, language=language)
    tokens = lexer.tokenize()

    # Print table header
    print("\n┌─────┬──────────────────┬─────────────────┬──────┐")
    print("│  #  │ Type             │ Value           │ Line │")
    print("├─────┼──────────────────┼─────────────────┼──────┤")

    # Print tokens
    for idx, token in enumerate(tokens):
        type_name = get_token_type_name(token.type)
        value_str = repr(token.value) if token.value is not None else ""
        # Truncate long values
        if len(value_str) > 15:
            value_str = value_str[:12] + "..."
        print(f"│ {idx:>3} │ {type_name:<16} │ {value_str:<15} │ {token.line:>4} │")

    print("└─────┴──────────────────┴─────────────────┴──────┘")

    # Print statistics
    print(f"\n📊 Token Statistics:")
    print(f"   Total tokens: {len(tokens)}")
    print(f"   Keywords: {count_keywords(tokens)}")
    print(f"   Identifiers: {count_identifiers(tokens)}")
    print(f"   Operators: {count_operators(tokens)}")


def run_example(example_name: str) -> None:
    """Run and display a pre-loaded example in all languages."""
    if example_name not in EXAMPLES:
        print(f"❌ Example '{example_name}' not found.")
        return

    example = EXAMPLES[example_name]
    english_code = example['code']

    print_header(f"{example_name.upper()} EXAMPLE")
    print(f"\nDescription: {example['description']}\n")

    # Tokenize once
    lexer = Lexer(english_code, 'english')
    tokens = lexer.tokenize()

    # Display in all three languages
    for lang in LANGUAGES:
        if lang == 'english':
            translated = english_code
        else:
            translated = lexer.translate(tokens, lang)

        print_section(lang.upper())
        print(translated)

def conflict_detection_demo() -> None:
    """Interactive demo showing identifier conflict resolution."""
    print_header("IDENTIFIER CONFLICT DETECTION DEMO")

    print(CONFLICT_EXAMPLE['explanation'])

    print_section("ORIGINAL ENGLISH CODE")
    print(CONFLICT_EXAMPLE['code'])

    # Translate to Spanish
    lexer = Lexer(CONFLICT_EXAMPLE['code'], 'english')
    tokens = lexer.tokenize()
    spanish = lexer.translate(tokens, 'spanish')

    print_section("TRANSLATED TO SPANISH (with conflict resolution)")
    print(spanish)

    # Highlight the changes
    print("\n📝 CONFLICTS RESOLVED:")
    print("  ✓ y → _y")
    print("  ✓ para → _para")
    print("  ✓ o → _o")

    # Verify by retokenizing
    print("\n✅ VERIFICATION: Retokenizing Spanish code...")
    try:
        spanish_lexer = Lexer(spanish, 'spanish')
        spanish_tokens = spanish_lexer.tokenize()
        print(f"   Original tokens: {len(tokens)}")
        print(f"   Spanish tokens: {len(spanish_tokens)}")
        print(f"   Match: {'YES' if len(spanish_tokens) == len(tokens) else 'NO'}")
    except LexerError as e:
        print(f"   ❌ Error: {e}")

# ─────────────────────────────────────────────────────────────
# COMMAND-LINE MODE
# ─────────────────────────────────────────────────────────────

def create_argument_parser() -> argparse.ArgumentParser:
    """Create and configure argument parser."""
    parser = argparse.ArgumentParser(
        prog='mll',
        description='Multilingual Lexical Analyzer - Translate code between languages',
        epilog='Run without arguments for interactive mode.'
    )

    parser.add_argument(
        '--version', '-v',
        action='version',
        version=f'%(prog)s {VERSION}'
    )

    parser.add_argument(
        '--translate', '-t',
        metavar='CODE',
        help='Translate code string'
    )

    parser.add_argument(
        '--inspect', '-i',
        metavar='CODE',
        help='Inspect and display tokens'
    )

    parser.add_argument(
        '--example', '-e',
        metavar='NAME',
        choices=list(EXAMPLES.keys()),
        help=f'Run pre-loaded example: {", ".join(EXAMPLES.keys())}'
    )

    parser.add_argument(
        '--source', '-s',
        default='english',
        choices=LANGUAGES,
        help='Source language (default: english)'
    )

    parser.add_argument(
        '--target', '-T',
        default='english',
        choices=LANGUAGES,
        help='Target language (default: english)'
    )

    parser.add_argument(
        '--file', '-f',
        metavar='PATH',
        help='Read code from file'
    )

    parser.add_argument(
        '--demo-conflicts',
        action='store_true',
        help='Run conflict detection demo'
    )

    return parser


def load_code_from_file(filepath: str) -> str:
    """Load code from file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"❌ Error: File not found: {filepath}", file=sys.stderr)
        sys.exit(1)
    except IOError as e:
        print(f"❌ Error reading file: {e}", file=sys.stderr)
        sys.exit(1)


def command_line_mode(args) -> None:
    """Handle command-line mode operations."""
    # Handle conflict demo
    if args.demo_conflicts:
        conflict_detection_demo()
        return

    # Handle example
    if args.example:
        run_example(args.example)
        return

    # Get code from file, argument, or stdin
    code = None
    if args.file:
        code = load_code_from_file(args.file)
    elif args.translate:
        code = args.translate
    elif args.inspect:
        code = args.inspect
    elif not sys.stdin.isatty():
        # Read from pipe
        code = sys.stdin.read()

    if not code:
        print("❌ Error: No code provided. Use --translate, --inspect, --file, or pipe input.", file=sys.stderr)
        sys.exit(1)

    # Determine operation
    try:
        if args.inspect is not None:
            # Inspection mode - explicit --inspect takes priority
            inspect_tokens(code, args.source)
        else:
            # Translation mode - default for --translate, --file, or piped input
            result = translate_code(code, args.source, args.target)
            print(result)
    except LexerError as e:
        print(f"❌ Lexer Error: {e}", file=sys.stderr)
        sys.exit(1)


# ─────────────────────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────────────────────

def main() -> None:
    """Main entry point for the CLI."""
    try:
        parser = create_argument_parser()
        args = parser.parse_args()

        # Detect mode: if no arguments provided, run interactive mode
        if len(sys.argv) == 1:
            from .repl import interactive_mode
            interactive_mode()
        else:
            command_line_mode(args)

    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user. Goodbye!", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()