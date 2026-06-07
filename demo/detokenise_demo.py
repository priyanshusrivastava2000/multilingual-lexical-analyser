# Demonstrate cross-language translation

from multilang_lexer import Lexer

def main():
    print("\n" + "=" * 60)
    print("BIDIRECTIONAL TRANSLATION DEMO")
    print("=" * 60)

    spanish_code = '''
local función factorial(n)
    si n <= 1 entonces
        devolver 1
    sino
        devolver n * factorial(n - 1)
    fin
fin
'''

    print("\nOriginal Spanish code:")
    print("-" * 60)
    print(spanish_code)

    # Tokenize Spanish code
    lexer = Lexer(spanish_code, language='spanish')
    tokens = lexer.tokenize()

    # Translate to English
    print("\nSpanish → English:")
    print("-" * 60)
    english_output = lexer.translate(tokens, 'english')
    print(english_output)

    # Translate to Mandarin
    print("\n\nSpanish → Mandarin:")
    print("-" * 60)
    mandarin_output = lexer.translate(tokens, 'mandarin')
    print(mandarin_output)

if __name__ == "__main__":
    main()
