import re

numerical_mappings = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}
numerical_mappings_reversed = {
    key[::-1]: value for key, value in numerical_mappings.items()
}

file = open("day1.txt", "r")
lines = file.readlines()
cleaned = [line.strip() for line in lines]
calibrations = []


def find_first_digit(line: str, pattern: str, mapping: dict[str, str]) -> str:
    match = re.search(pattern, line)
    if match:
        val = match.group(0)
        if val.isdigit():
            return val
        else:
            return mapping[val]
    return "0"


for line in cleaned:
    # for line in [
    #     "two1nine",
    #     "eightwothree",
    #     "abcone2threexyz",
    #     "xtwone3four",
    #     "4nineeightseven2",
    #     "zoneight234",
    #     "7pqrstsixteen",
    # ]:
    first_digit = find_first_digit(
        line, "|".join([*numerical_mappings.keys(), "\d"]), numerical_mappings
    )
    last_digit = find_first_digit(
        line[::-1],
        "|".join([*numerical_mappings_reversed.keys(), "\d"]),
        numerical_mappings_reversed,
    )
    calibration = first_digit + last_digit
    calibrations.append(int(calibration))
print(calibrations)
print(sum(calibrations))
