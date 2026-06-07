local función calculate_average(scores)
    local sum = 0
    local count = 0

    para i = 1, # scores hacer
        sum = sum + scores[i]
        count = count + 1
    fin

    si count > 0 entonces
        devolver sum / count
    sino
        devolver 0
    fin
fin

local función get_letter_grade(average)
    si average >= 90 entonces
        devolver "A"
    osi average >= 80 entonces
        devolver "B"
    osi average >= 70 entonces
        devolver "C"
    osi average >= 60 entonces
        devolver "D"
    sino
        devolver "F"
    fin
fin

local math_scores = { 85, 92, 78, 95, 88 }
local science_scores = { 90, 85, 88, 92, 87 }

local math_avg = calculate_average(math_scores)
local science_avg = calculate_average(science_scores)

local math_grade = get_letter_grade(math_avg)
local science_grade = get_letter_grade(science_avg)

print("Math Average: " .. math_avg .. " (Grade: " .. math_grade .. ")")
print("Science Average: " .. science_avg .. " (Grade: " .. science_grade .. ")")
