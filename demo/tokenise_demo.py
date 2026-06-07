"""
Demo script for the multilingual lexical analyzer.
Shows tokenization in English, Spanish, and Mandarin.
Demonstrates the "in" keyword support in for-in loops.
"""

from multilang_lexer import Lexer


def main():
    # Test code in English (demonstrating the "in" keyword)
    english_code = '''
local function sum_table(t)
    local total = 0
    for k, v in pairs(t) do
        total = total + v
    end
    return total
end
'''

    # Test code in Spanish (demonstrating the "en" keyword)
    spanish_code = '''
local función sum_table(t)
    local total = 0
    para k, v en pairs(t) iterar
        total = total + v
    fin
    devolver total
fin
'''

    # Test code in Mandarin (demonstrating the "在" keyword)
    mandarin_code = '''
本地 函数 sum_table(t)
    本地 total = 0
    为 k, v 在 pairs(t) 执行
        total = total + v
    结束
    返回 total
结束
'''

    # Tokenize each language
    eng_lexer = Lexer(english_code, language='english')
    spa_lexer = Lexer(spanish_code, language='spanish')
    man_lexer = Lexer(mandarin_code, language='mandarin')

    eng_tokens = eng_lexer.tokenize()
    spa_tokens = spa_lexer.tokenize()
    man_tokens = man_lexer.tokenize()

    # Display results
    print("English  | Spanish  | Mandarin | Match")
    print("-" * 50)

    all_match = True
    for i in range(len(eng_tokens)):
        eng = eng_tokens[i].type
        spa = spa_tokens[i].type
        man = man_tokens[i].type
        match = "YES" if eng == spa == man else "NO"
        if match == "NO":
            all_match = False
        print(f"{eng:<8} | {spa:<8} | {man:<8} | {match}")

    print("-" * 50)
    print(f"All tokens match: {all_match}")


if __name__ == "__main__":
    main()
