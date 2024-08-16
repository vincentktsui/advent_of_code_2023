import math
from collections import defaultdict

file = open("day8.txt", "r")
lines = file.readlines()
cleaned = [line.strip() for line in lines]
sequence = cleaned[0]
mappings_temp = cleaned[2:]

mapping = {}
for m in mappings_temp:
    split = m.split("=")
    k = split[0].strip()
    v = split[1].replace("(", "").replace(")", "").replace(" ", "").split(",")
    mapping[k] = v


# steps = 0
# current_sequence = sequence
# current = "AAA"
# while current != "ZZZ":
#     if not current_sequence:
#         current_sequence = sequence
#     d = current_sequence[0]
#     current_sequence = current_sequence[1:]
#     l = 0 if d == "L" else 1
#     steps += 1
#     current = mapping[current][l]
def calc_steps(starting):
    steps = 0
    current_sequence = sequence
    current = starting
    while current[-1] != "Z":
        if not current_sequence:
            current_sequence = sequence
        d = current_sequence[0]
        current_sequence = current_sequence[1:]
        l = 0 if d == "L" else 1
        steps += 1
        current = mapping[current][l]
    return steps


all_starting = [x for x in mapping.keys() if x[-1] == "A"]
steps = [calc_steps(x) for x in all_starting]
print(math.lcm(*steps))
