import functools

file = open("day15.txt", "r")
lines = file.readlines()

sequences = lines[0].strip().split(",")
print(sequences)

@functools.cache
def step(c, start):
    temp = start + ord(c)
    temp *= 17
    temp %= 256
    return temp

@functools.cache
def hash_string(seq):
    temp = 0
    for c in seq:
        temp = step(c, temp)
    return temp

sum = 0
for seq in sequences:
    sum += hash_string(seq)

print(sum)


# boxes
boxes = {key: [] for key in range(256)}
labels = {}

for seq in sequences:
    if "-" in seq:
        label, _ = seq.split("-")
        box = hash_string(label)
        if label in labels:
            del labels[label]
            idx = boxes[box].index(label)
            del boxes[box][idx]
    elif "=" in seq:
        label, power = seq.split("=")
        box = hash_string(label)
        if label not in labels:
            boxes[box].append(label)
        labels[label] = power

total = 0
for box_num, lenses in boxes.items():
    if len(lenses):
        for i in range(len(lenses)):
            label = lenses[i]
            power = int(labels[label])
            total += (i+1) * (box_num + 1) * power
print(total)
        