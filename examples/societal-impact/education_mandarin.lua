本地 函数 calculate_average(scores)
    本地 sum = 0
    本地 count = 0

    对于 i = 1, # scores 执行
        sum = sum + scores[i]
        count = count + 1
    结束

    如果 count > 0 那么
        返回 sum / count
    否则
        返回 0
    结束
结束

本地 函数 get_letter_grade(average)
    如果 average >= 90 那么
        返回 "A"
    否则如果 average >= 80 那么
        返回 "B"
    否则如果 average >= 70 那么
        返回 "C"
    否则如果 average >= 60 那么
        返回 "D"
    否则
        返回 "F"
    结束
结束

本地 math_scores = { 85, 92, 78, 95, 88 }
本地 science_scores = { 90, 85, 88, 92, 87 }

本地 math_avg = calculate_average(math_scores)
本地 science_avg = calculate_average(science_scores)

本地 math_grade = get_letter_grade(math_avg)
本地 science_grade = get_letter_grade(science_avg)

print("Math Average: " .. math_avg .. " (Grade: " .. math_grade .. ")")
print("Science Average: " .. science_avg .. " (Grade: " .. science_grade .. ")")
