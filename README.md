# multilingual-lexical-analyser

[![CI](https://github.com/YOUR_USERNAME/multilingual-lexical-analyser/actions/workflows/ci.yml/badge.svg)](https://github.com/YOUR_USERNAME/multilingual-lexical-analyser/actions/workflows/ci.yml)

A multilingual lexical analyzer that tokenizes and translates Lua-like code across English, Spanish, and Mandarin. Keywords are defined in JSON files, making the system straightforward to extend.

## Installation

### From GitHub

```shell
git clone https://github.com/priyanshusrivastava2000/multilingual-lexical-analyser.git
cd multilingual-lexical-analyser
pip install .
```

### Development install (editable)

```shell
pip install -e ".[dev]"
```

**Requirements:** Python 3.8 or higher, no external dependencies.

## Interactive CLI

The package installs an `mll` command for exploring multilingual code translation.

### Quick Start

```bash
# Launch interactive REPL
mll

# Direct translation via command-line args
mll --translate "if x then y end" --source english --target spanish
```

### Interactive Mode

The REPL provides a state-based interface:

**States:**
- **Empty** — no code loaded; prompts you to load code
- **Source** — code loaded as text; can tokenize or reload
- **Tokenized** — code converted to tokens; can translate or reload

**Workflow:**
1. **Load Code** — manual entry, file path, or pre-loaded example
2. **Tokenize** — view the token stream with statistics
3. **Detokenize / Translate** — output code in any supported language

**Example session:**
```
No code loaded. Please load code to begin.

OPTIONS:
  1. Load Code
  2. Exit

Choice [1-2]: 1
```

After loading:
```
✓ Code loaded (50 characters, english)
════════════════════════════════════════════════════════════

📄 Language: English
────────────────────────────────────────────────────────────
local x = 10
local y = 20
────────────────────────────────────────────────────────────

OPTIONS:
  1. Load Code
  2. Tokenize
  3. Exit
```

After tokenizing:
```
🔢 Tokenized Code - Language: English
────────────────────────────────────────────────────────────

┌─────┬──────────────────┬─────────────────┬──────┐
│  #  │ Type             │ Value           │ Line │
├─────┼──────────────────┼─────────────────┼──────┤
│   0 │ TK_LOCAL         │                 │    1 │
│   1 │ TK_NAME          │ 'x'             │    1 │
│   2 │ CHAR('=')        │                 │    1 │
│   3 │ TK_NUMBER        │ 10.0            │    1 │
└─────┴──────────────────┴─────────────────┴──────┘

📊 Token Statistics:
   Total tokens: 9
   Keywords: 2
   Identifiers: 2
   Operators: 2

OPTIONS:
  1. Load Code
  2. Detokenize (translate)
  3. Exit
```

### Command-Line Usage

```bash
# Translate a code string
mll --translate "local x = 5" --source english --target spanish
mll -t "if x then y end" -s english -T mandarin

# Inspect token stream
mll --inspect "function test() end" --source english
mll -i "función prueba() fin" -s spanish

# Run a pre-loaded example
mll --example factorial --target spanish
mll -e fibonacci

# Translate a file
mll --file script.lua --translate --target mandarin
mll -f code.lua -t -T spanish

# Pipe input
cat script.lua | mll --translate --target spanish

# Run conflict detection demo
mll --demo-conflicts
```

### Available Examples

| Name | Description |
|------|-------------|
| `factorial` | Recursive factorial calculation |
| `fibonacci` | Recursive Fibonacci sequence |
| `loop` | Iterative sum with for loop |
| `conditional` | Find maximum of two numbers |

## Programmatic API

### Basic Usage

```python
from multilang_lexer import Lexer, Token, TokenType, LexerError

# Tokenize entire source
lexer = Lexer("if x then y end", language='english')
tokens = lexer.tokenize()  # list of Token objects

# Get tokens one at a time
lexer = Lexer("local x = 10", language='english')
token = lexer.lex()  # Token(type=TK_LOCAL, value=None, line=1)
```

### Cross-Language Translation

```python
from multilang_lexer import Lexer

lexer = Lexer("if x then y end", language='english')
tokens = lexer.tokenize()

spanish_code = lexer.translate(tokens, 'spanish')
# "si x entonces y fin"

mandarin_code = lexer.translate(tokens, 'mandarin')
# "如果 x 那么 y 结束"

english_code = lexer.translate(tokens, 'english')
# or: lexer.translate_to_english(tokens)
```

### Automatic Conflict Resolution

Identifiers that clash with target language keywords are automatically prefixed with `_`:

```python
from multilang_lexer import Lexer

# "y" is Spanish for "and"; "para" for "for"; "o" for "or"
code = "local function process(y, para, o) return y and para end"
lexer = Lexer(code, language='english')
tokens = lexer.tokenize()

spanish = lexer.translate(tokens, 'spanish')
# "local función process ( _y , _para , _o ) devolver _y y _para fin"
```

### Working with Tokens

```python
from multilang_lexer import Lexer, TokenType

lexer = Lexer("local x = 10", language='english')
tokens = lexer.tokenize()

for token in tokens:
    print(f"Type: {token.type}, Value: {token.value}, Line: {token.line}")

keywords    = [t for t in tokens if t.type in [TokenType.TK_IF, TokenType.TK_LOCAL]]
identifiers = [t for t in tokens if t.type == TokenType.TK_NAME]
```

### Error Handling

```python
from multilang_lexer import Lexer, LexerError

try:
    lexer = Lexer('local x = "unterminated string', language='english')
    tokens = lexer.tokenize()
except LexerError as e:
    print(f"Lexer error: {e}")
    # Lexer error: unfinished string at line 1 near '<string>'
```

### Supported Languages

| Language | Code | Example keyword |
|----------|------|-----------------|
| English | `'english'` | `if`, `then`, `end` |
| Spanish | `'spanish'` | `si`, `entonces`, `fin` |
| Mandarin | `'mandarin'` | `如果`, `那么`, `结束` |

Language definitions live in `src/multilang_lexer/languages/` as JSON files and can be edited to add new keywords or add support for additional languages.

## Testing

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=multilang_lexer

# Run a specific test file
pytest tests/test_lexer.py

# Run a specific test with verbose output
pytest tests/test_lexer.py::test_lexer_spanish_keywords -v
```

**Test modules:**
- `tests/test_tokens.py` — token type recognition
- `tests/test_lexer.py` — core lexer functionality and language support
- `tests/test_languages.py` — language-specific keyword tests
- `tests/test_detokenizer.py` — translation and detokenization

## Demo Scripts

```bash
python demo/tokenise_demo.py      # tokenize across all three languages
python demo/detokenise_demo.py    # bidirectional translation demo
```

## Contributing

1. Fork the repository and create a feature branch.
2. Install in development mode: `pip install -e ".[dev]"`
3. Add tests for any new behaviour.
4. Run `pytest` and confirm all tests pass.
5. Open a pull request.

To add a new language, create `src/multilang_lexer/languages/<language>.json` following the same keyword structure as the existing files.

## License

MIT — see [LICENSE](LICENSE).
