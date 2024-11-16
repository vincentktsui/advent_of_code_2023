file = open("day13.txt", "r")
lines = file.readlines()
horizontal_patterns = []
new_map = []
for line in lines:
    stripped_line = line.strip()
    if not stripped_line:
        horizontal_patterns.append(new_map)
        new_map = []
    else:
        new_map.append(stripped_line)
horizontal_patterns.append(new_map)

vertical_patterns = []
for pattern in horizontal_patterns:
    new_pattern = []
    for i in range(len(pattern[0])):
        column = ""
        for j in range(len(pattern)):
            column+= pattern[j][i]
        new_pattern.append(column)
    vertical_patterns.append(new_pattern)

def mirror(pat1, pat2):
    middle = len(pat1)
    shorter = min(len(pat1), len(pat2))
    for i in range(shorter):
        if pat1[middle - 1 - i] != pat2[i]:
            return False
    return True

def mirror_difference(pat1, pat2):
    middle = len(pat1)
    shorter = min(len(pat1), len(pat2))
    total_differences = 0
    for i in range(shorter):
        x = pat1[middle - 1 - i]
        y = pat2[i]
        total_differences += sum([1 for a, b in zip(x, y) if a != b])
    return total_differences

# calc = 0
# temp = []
# for num in range(len(horizontal_patterns)):
#     hor = horizontal_patterns[num]
#     ver = vertical_patterns[num]
#     before = len(temp)
#     for i in range(1, len(hor)):
#         if mirror(hor[:i], hor[i:]):
#             calc += 100 * i
#             temp.append(("horizontal", i))
#     for i in range(1, len(ver)):
#         if mirror(ver[:i], ver[i:]):
#             calc += i
#             temp.append(("vertical", i))
#     after = len(temp)
#     if before == after:
#         print(num)
# print(calc)

calc = 0
for num in range(len(horizontal_patterns)):
    hor = horizontal_patterns[num]
    ver = vertical_patterns[num]
    for i in range(1, len(hor)):
        if mirror_difference(hor[:i], hor[i:]) == 1:
            calc += 100 * i
    for i in range(1, len(ver)):
        if mirror_difference(ver[:i], ver[i:]) == 1:
            calc += i
print(calc)


