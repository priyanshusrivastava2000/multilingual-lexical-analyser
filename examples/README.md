# Examples

Practical examples demonstrating the multilingual lexical analyzer.

## Demo Scripts

Both scripts live in the `demo/` directory and can be run directly after installing the package.

### Tokenization Demo

**File**: [demo/tokenise_demo.py](../demo/tokenise_demo.py)

Shows how equivalent code in English, Spanish, and Mandarin produces identical token streams.

```bash
python demo/tokenise_demo.py
```

### Translation Demo

**File**: [demo/detokenise_demo.py](../demo/detokenise_demo.py)

Shows bidirectional translation between languages — Spanish → English and Spanish → Mandarin.

```bash
python demo/detokenise_demo.py
```

## Societal Impact: Educational Access

### Educational Examples

**Directory**: [societal-impact/](societal-impact/)

Functionally identical grade-calculator programs written in each supported language:

- [education_english.lua](societal-impact/education_english.lua)
- [education_spanish.lua](societal-impact/education_spanish.lua)
- [education_mandarin.lua](societal-impact/education_mandarin.lua)

**Documentation:**
- [comparison.md](societal-impact/comparison.md) — side-by-side language comparison
- [impact_statement.md](societal-impact/impact_statement.md) — analysis of educational accessibility benefits

These examples show how students can learn programming logic in their native language and have their code seamlessly translated, removing English as a prerequisite.

## Using the CLI with Examples

Make sure the package is installed first:

```bash
pip install .
```

Then inspect or translate any file:

```bash
# Inspect tokens
mll -f examples/societal-impact/education_spanish.lua -s spanish -i ""
mll -f examples/societal-impact/education_mandarin.lua -s mandarin -i ""

# Translate between languages
mll -f examples/societal-impact/education_spanish.lua -s spanish -T english
mll -f examples/societal-impact/education_mandarin.lua -s mandarin -T spanish
mll -f examples/societal-impact/education_english.lua -s english -T mandarin
```

Or use **interactive mode**:

```bash
mll
# Select: Load Code → Load from file → choose a file and language
```

## Adding Your Own Language

Create `src/multilang_lexer/languages/<name>.json` using the same keyword structure as the existing files, then reinstall the package:

```bash
pip install -e .
mll -t "if x then y end" -s english -T <name>
```

## Resources

- Main documentation: [../README.md](../README.md)
- Language definitions: [../src/multilang_lexer/languages/](../src/multilang_lexer/languages/)
- Test suite: [../tests/](../tests/)
