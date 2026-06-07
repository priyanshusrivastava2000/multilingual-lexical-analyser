local function calculate_average(scores)
    local sum = 0
    local count = 0
    
    for i = 1, #scores do
        sum = sum + scores[i]
        count = count + 1
    end
    
    if count > 0 then
        return sum / count
    else
        return 0
    end
end

local function get_letter_grade(average)
    if average >= 90 then
        return "A"
    elseif average >= 80 then
        return "B"
    elseif average >= 70 then
        return "C"
    elseif average >= 60 then
        return "D"
    else
        return "F"
    end
end

local math_scores = {85, 92, 78, 95, 88}
local science_scores = {90, 85, 88, 92, 87}

local math_avg = calculate_average(math_scores)
local science_avg = calculate_average(science_scores)

local math_grade = get_letter_grade(math_avg)
local science_grade = get_letter_grade(science_avg)

print("Math Average: " .. math_avg .. " (Grade: " .. math_grade .. ")")
print("Science Average: " .. science_avg .. " (Grade: " .. science_grade .. ")")
