"""
Interactive REPL mode for the multilingual lexical analyzer.
Provides an interactive command-line interface for loading, tokenizing, and translating code.
"""

import sys
from typing import Optional, List
from multilang_lexer import Lexer
from multilang_lexer.tokens import Token
from multilang_lexer.exceptions import LexerError

# Import shared utilities from cli module
from .cli import (
    LANGUAGES,
    VERSION,
    EXAMPLES,
    print_header,
    print_section,
    inspect_tokens,
    translate_code,
    load_code_from_file,
    get_token_type_name,
    count_keywords,
    count_identifiers,
    count_operators,
)

# ─────────────────────────────────────────────────────────────
# STATE CONSTANTS
# ─────────────────────────────────────────────────────────────

STATE_EMPTY = 'empty'           # No code loaded
STATE_SOURCE = 'source'         # Source code loaded
STATE_TOKENIZED = 'tokenized'   # Code tokenized


# ─────────────────────────────────────────────────────────────
# INPUT UTILITIES
# ─────────────────────────────────────────────────────────────

def choose_language(prompt: str) -> str:
    """Prompt user to choose a language."""
    print(f"\n{prompt}:")
    for i, lang in enumerate(LANGUAGES, 1):
        print(f"  {i}. {lang.capitalize()}")

    while True:
        try:
            choice = input("Choice [1-3]: ").strip()
            idx = int(choice) - 1
            if 0 <= idx < len(LANGUAGES):
                return LANGUAGES[idx]
            print("Invalid choice. Please enter 1, 2, or 3.")
        except (ValueError, EOFError):
            print("Invalid input. Please enter a number 1-3.")


def read_multiline_code() -> str:
    """Read multiline code from stdin."""

    # Platform-specific EOF instruction
    eof_key = "Ctrl+Z then Enter" if sys.platform == "win32" else "Ctrl+D"
    print(f"\nEnter code (press {eof_key} on empty line to finish):")

    print('─' * 60)
    lines = []
    try:
        while True:
            line = input()
            lines.append(line)
    except EOFError:
        pass

    return '\n'.join(lines)

def get_menu_choice(max_choice: int) -> int:
    """Get valid menu choice from user."""
    while True:
        try:
            choice = input(f"\nChoice [1-{max_choice}]: ").strip()
            num = int(choice)
            if 1 <= num <= max_choice:
                return num
            print(f"Invalid choice. Please enter 1-{max_choice}.")
        except (ValueError, EOFError):
            print(f"Invalid input. Please enter a number 1-{max_choice}.")
        except KeyboardInterrupt:
            raise

# ─────────────────────────────────────────────────────────────
# DISPLAY FUNCTIONS
# ─────────────────────────────────────────────────────────────

def display_source_code(code: str, language: str) -> None:
    """Display source code with language header."""
    print(f"\n📄 Language: {language.capitalize()}")
    print('─' * 60)

    # Split code into lines and limit display
    lines = code.split('\n')
    max_lines = 100

    if len(lines) <= max_lines:
        print(code)
    else:
        # Show first max_lines lines with a truncation message
        print('\n'.join(lines[:max_lines]))
        print(f"\n... ({len(lines) - max_lines} more lines)")

    print('─' * 60)


def display_tokenized_view(tokens: List[Token], language: str) -> None:
    """Display tokenized code as table with statistics."""
    print(f"\n🔢 Tokenized Code - Language: {language.capitalize()}")
    print('─' * 60)

    # Print token table header
    print("\n┌─────┬──────────────────┬─────────────────┬──────┐")
    print("│  #  │ Type             │ Value           │ Line │")
    print("├─────┼──────────────────┼─────────────────┼──────┤")

    # Print tokens (limit to reasonable number)
    max_tokens_display = 50
    tokens_to_show = tokens[:max_tokens_display]

    for idx, token in enumerate(tokens_to_show):
        type_name = get_token_type_name(token.type)
        value_str = repr(token.value) if token.value is not None else ""
        # Truncate long values
        if len(value_str) > 15:
            value_str = value_str[:12] + "..."
        print(f"│ {idx:>3} │ {type_name:<16} │ {value_str:<15} │ {token.line:>4} │")

    if len(tokens) > max_tokens_display:
        print(f"│ ... │ ({len(tokens) - max_tokens_display} more tokens)")
        print("└─────┴──────────────────┴─────────────────┴──────┘")
    else:
        print("└─────┴──────────────────┴─────────────────┴──────┘")

    # Print statistics
    print(f"\n📊 Token Statistics:")
    print(f"   Total tokens: {len(tokens)}")
    print(f"   Keywords: {count_keywords(tokens)}")
    print(f"   Identifiers: {count_identifiers(tokens)}")
    print(f"   Operators: {count_operators(tokens)}")
    print('─' * 60)


def display_menu(state: str) -> None:
    """Display menu options based on current state."""
    print("\nOPTIONS:")

    if state == STATE_EMPTY:
        print("  1. Load Code")
        print("  2. Exit")
    elif state == STATE_SOURCE:
        print("  1. Load Code")
        print("  2. Tokenize")
        print("  3. Exit")
    elif state == STATE_TOKENIZED:
        print("  1. Load Code")
        print("  2. Detokenize (translate)")
        print("  3. Exit")


# ─────────────────────────────────────────────────────────────
# INTERACTIVE WORKFLOWS
# ─────────────────────────────────────────────────────────────

def load_code_interactive() -> tuple[Optional[str], Optional[str]]:
    """Interactive code loading workflow. Returns (code, language) or (None, None)."""
    print("\n" + "═" * 60)
    print("LOAD CODE:")
    print("  1. Enter code manually")
    print("  2. Load from file")
    print("  3. Load pre-loaded example")
    print("  4. Cancel")

    choice = get_menu_choice(4)

    if choice == 1:
        # Manual entry
        language = choose_language("Code language")
        code = read_multiline_code()
        if not code.strip():
            print("\n❌ No code entered.")
            return None, None
        return code, language

    elif choice == 2:
        # Load from file
        filepath = input("\nFile path: ").strip()
        if not filepath:
            print("\n❌ No file path entered.")
            return None, None
        try:
            code = load_code_from_file(filepath)
            language = choose_language("Code language")
            return code, language
        except SystemExit:
            return None, None

    elif choice == 3:
        # Pre-loaded example
        print("\nAvailable examples:")
        example_list = list(EXAMPLES.keys())
        for i, name in enumerate(example_list, 1):
            desc = EXAMPLES[name]['description']
            print(f"  {i}. {name.capitalize():<12} - {desc}")

        ex_choice = get_menu_choice(len(example_list))
        example_name = example_list[ex_choice - 1]
        code = EXAMPLES[example_name]['code']
        print(f"\n✓ Loaded '{example_name}' example")
        return code, 'english'  # Examples are in English

    else:  # Cancel
        return None, None


# ─────────────────────────────────────────────────────────────
# ACTION FUNCTIONS
# ─────────────────────────────────────────────────────────────

def tokenize_action(code: str, language: str) -> tuple[Optional[List[Token]], str]:
    """
    Tokenize the source code and return tokens.
    Returns (tokens, state) where state is STATE_TOKENIZED on success or STATE_SOURCE on error.
    """
    try:
        lexer = Lexer(code, language=language)
        tokens = lexer.tokenize()
        return tokens, STATE_TOKENIZED
    except LexerError as e:
        print(f"\n❌ Lexer Error: {e}")
        print("Staying in source view.")
        return None, STATE_SOURCE


def detokenize_action(tokens: List[Token], current_language: str) -> tuple[Optional[str], Optional[str], str]:
    """
    Detokenize (translate) tokens to target language.
    Returns (translated_code, new_language, state) where state is STATE_SOURCE on success.
    """
    target = choose_language("Target language")

    try:
        # Create a lexer with current language to access the translate method
        # We need to reconstruct source code first, then translate
        lexer = Lexer("", language=current_language)  # Dummy code, we'll use tokens directly
        translated = lexer.translate(tokens, target)

        print(f"\n✓ Translated from {current_language} to {target}")
        return translated, target, STATE_SOURCE
    except LexerError as e:
        print(f"\n❌ Lexer Error: {e}")
        print("Staying in tokenized view.")
        return None, None, STATE_TOKENIZED


def show_help() -> None:
    """Display help and about information."""
    print_header("ABOUT & HELP")

    print(f"""
Multilingual Lexical Analyzer v{VERSION}

This tool demonstrates cross-language code translation using a
multilingual lexer based on Lua 4.0's implementation.

FEATURES:
  • Translate code between English, Spanish, and Mandarin
  • Inspect token streams and types
  • Automatic identifier conflict resolution
  • Pre-loaded code examples

SUPPORTED LANGUAGES:
  • English  - Standard Lua-like syntax
  • Spanish  - Keywords in Spanish (si, entonces, función, etc.)
  • Mandarin - Keywords in Simplified Chinese

COMMAND-LINE USAGE:
  mll                                    # Interactive mode
  mll --translate "code" -s english -T spanish
  mll --inspect "code" -s mandarin
  mll --example factorial
  mll --file script.lua --translate -T spanish
""")


def interactive_mode() -> None:
    """Main interactive REPL loop with state machine."""
    print_header("Multilingual Lexical Analyzer - Interactive Mode")

    print(f"\nVersion {VERSION}")
    print("Load code, tokenize to inspect structure, and translate between languages.\n")

    # State variables
    current_state = STATE_EMPTY
    loaded_code = None
    loaded_language = None
    stored_tokens = None

    while True:
        try:
            # Print separator at top of loop (except first iteration when empty)
            if current_state != STATE_EMPTY or loaded_code is not None:
                print("\n" + "═" * 60)

            # Display current view based on state
            if current_state == STATE_SOURCE:
                display_source_code(loaded_code, loaded_language)
            elif current_state == STATE_TOKENIZED:
                display_tokenized_view(stored_tokens, loaded_language)
            else:  # STATE_EMPTY
                print("\nNo code loaded. Please load code to begin.")

            # Display menu based on state
            display_menu(current_state)

            # Determine max choice based on state
            if current_state == STATE_EMPTY:
                max_choice = 2
            else:  # SOURCE or TOKENIZED
                max_choice = 3

            choice = get_menu_choice(max_choice)

            # Handle choice based on state
            if choice == 1:
                # Load Code - available in all states
                code, language = load_code_interactive()
                if code:
                    loaded_code = code
                    loaded_language = language
                    stored_tokens = None  # Clear tokens when loading new code
                    current_state = STATE_SOURCE
                    print(f"\n✓ Code loaded ({len(code)} characters, {language})")

            elif choice == 2:
                if current_state == STATE_SOURCE:
                    # Tokenize
                    tokens, new_state = tokenize_action(loaded_code, loaded_language)
                    if tokens is not None:
                        stored_tokens = tokens
                        current_state = new_state

                elif current_state == STATE_TOKENIZED:
                    # Detokenize (translate)
                    translated, new_lang, new_state = detokenize_action(stored_tokens, loaded_language)
                    if translated is not None:
                        loaded_code = translated
                        loaded_language = new_lang
                        stored_tokens = None
                        current_state = new_state

                elif current_state == STATE_EMPTY:
                    # Exit
                    print("\n👋 Goodbye!")
                    break

            elif choice == 3:
                # Exit (only available in SOURCE and TOKENIZED states)
                print("\n👋 Goodbye!")
                break

        except KeyboardInterrupt:
            print("\n\n⚠️  Interrupted. Returning to main menu...")
            continue