# Educational Examples: Language Comparison

## Overview
This directory contains **functionally identical** programs written in three languages: English, Spanish, and Mandarin. Each program implements a grade calculator that demonstrates fundamental programming concepts.

## Programming Concepts Demonstrated

All three examples teach the same core concepts:

1. **Variables** - Storing data (scores, averages, grades)
2. **Functions** - Code organization and reusability
3. **Loops** - Iterating through arrays of scores
4. **Conditionals** - Making decisions (grade assignment)
5. **Arrays** - Managing collections of data
6. **Mathematical Operations** - Sum, division, comparison

## Side-by-Side Comparison

### Function Declaration

| English | Spanish | Mandarin |
|---------|---------|----------|
| `local function calculate_average(scores)` | `local función calcular_promedio(puntuaciones)` | `本地 函数 计算平均值(分数列表)` |

### Conditional Statement

| English | Spanish | Mandarin |
|---------|---------|----------|
| `if average >= 90 then` | `si promedio >= 90 entonces` | `如果 平均值 >= 90 那么` |
| `elseif average >= 80 then` | `osi promedio >= 80 entonces` | `否则如果 平均值 >= 80 那么` |
| `else` | `sino` | `否则` |
| `end` | `fin` | `结束` |

### Loop Structure

| English | Spanish | Mandarin |
|---------|---------|----------|
| `for i = 1, #scores do` | `para índice = 1, #puntuaciones hacer` | `对于 索引 = 1, #分数列表 执行` |
| `end` | `fin` | `结束` |

### Return Statement

| English | Spanish | Mandarin |
|---------|---------|----------|
| `return sum / count` | `retornar suma / contador` | `返回 总和 / 计数` |

## Verification

You can verify these programs are functionally identical by:

1. **Tokenizing each file:**
   ```bash
   mll tokenize education_english.lua --language english
   mll tokenize education_spanish.lua --language spanish
   mll tokenize education_mandarin.lua --language mandarin
   ```

2. **Translating between languages:**
   ```bash
   # Spanish to English
   mll translate education_spanish.lua --from spanish --to english
   
   # Mandarin to English
   mll translate education_mandarin.lua --from mandarin --to english
   ```

3. **Comparing token structures:**
   All three programs will produce identical token sequences (only the lexemes differ):
   - Same number of tokens
   - Same token types in the same order
   - Same logical structure and flow

## Learning Impact

These examples demonstrate that:

✅ **Programming logic is universal** - The same algorithm works regardless of keyword language

✅ **Native language reduces cognitive load** - Students can focus on concepts, not translation

✅ **Semantic meaning is preserved** - Variable names and comments match the keyword language

✅ **Cross-cultural collaboration is possible** - Code can be translated while maintaining logic

## Target Audience

- **Spanish-speaking students** in Latin America and Spain
- **Mandarin-speaking students** in China, Taiwan, and Chinese communities worldwide
- **Educational institutions** wanting to teach programming in native languages
- **Coding bootcamps** serving multilingual communities
- **Self-learners** who prefer to learn in their native language
